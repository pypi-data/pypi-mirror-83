# Definition and handling of candidates for ResolveLib
# Copyright (C) 2020  Nguyễn Gia Phong
#
# This file is part of offre.
#
# offre is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# offre is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with offre.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from functools import partial
from operator import attrgetter
from os.path import basename
from typing import Iterable, Sequence, Type
from urllib.parse import urldefrag

from distlib.wheel import Wheel
from html5lib import parse
from httpx import AsyncClient
from packaging.version import Version
from trio import (MemoryReceiveChannel, MemorySendChannel,
                  Nursery, open_memory_channel, open_nursery)

__all__ = ['Candidate', 'look']

SDIST_EXT = ('.tlz', '.tar.lz', '.tar.lzma', '.tar.xz', '.txz',
             '.tar.bz2', '.tbz', '.tar.gz', '.tgz', 'tar', '.zip')

sdist_version = re.compile('.+-(.+)').findall
parse_html5 = partial(parse, namespaceHTMLElements=False)


def removesuffix(string: str, *suffixes: str) -> str:
    """Return string without the first suffix found in the given ones."""
    for suffix in suffixes:
        if string.endswith(suffix): return string[:-len(suffix)]
    return string


class Candidate(ABC):
    """Candidate for use in ResolveLib."""

    version: Version

    @abstractmethod
    def __init__(self, name: str, url: str, fragment: str):
        self.name, self.url, self.hash = name, url, fragment

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {self.name} {self.version}>'

    def __str__(self) -> str:
        return f'{self.name} {self.version}'


class SdistCandidate(Candidate):
    """Candidate backed by a source distribution."""

    def __init__(self, name: str, url: str, fragment: str):
        super().__init__(name, url, fragment)
        base = removesuffix(basename(url).lower(), *SDIST_EXT)
        try:
            version, = sdist_version(base)
        except ValueError:
            raise ValueError('invalid filename') from None
        self.version = Version(version)


class WheelCandidate(Candidate):
    """Candidate backed by a wheel."""

    def __init__(self, name: str, url: str, fragment: str):
        super().__init__(name, url, fragment)
        self.version = Version(Wheel(url).version)


def classify_candidate(file: str) -> Type[Candidate]:
    """Return the candidate class to be backed by the given file."""
    if any(map(file.endswith, SDIST_EXT)): return SdistCandidate
    if file.endswith('.whl'): return WheelCandidate
    raise ValueError('unsupported filetype')


async def scrape(project: str, repository: AsyncClient,
                 send_channel: MemorySendChannel) -> None:
    """Scrape for candidates for project in the given repository."""
    async with send_channel:
        response = await repository.get(f'/{project}/')
        if response.is_error: return  # TODO: say something about this
        for a in parse_html5(response.text).iterfind('.//a'):
            url, fragment = urldefrag(a.get('href'))
            if url is None or basename(url) != a.text: continue
            cls = classify_candidate(url.lower())
            await send_channel.send(cls(project, url, fragment))


async def see(project: str, repositories: Iterable[AsyncClient],
              send_channel: MemorySendChannel, nursery: Nursery) -> None:
    """Start tasks that actually scrape the repositories.

    This must be run in a different task from `look`
    to close send_channel before finishing looping on receive_channel.
    """
    async with send_channel:
        for repository in repositories:
            nursery.start_soon(scrape, project, repository,
                               send_channel.clone())


async def look(project: str,
               repositories: Iterable[AsyncClient]) -> Sequence[Candidate]:
    """Look for the project's candidates in the given repositories."""
    send_channel: MemorySendChannel
    receive_channel: MemoryReceiveChannel
    send_channel, receive_channel = open_memory_channel(0)
    async with open_nursery() as nursery, receive_channel:
        nursery.start_soon(see, project, repositories, send_channel, nursery)
        result = [candidate async for candidate in receive_channel]
        result.sort(key=attrgetter('version'), reverse=True)
        return result
