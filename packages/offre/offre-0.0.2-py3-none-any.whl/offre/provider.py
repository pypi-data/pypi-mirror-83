# Provider for ResolveLib
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

from contextlib import AsyncExitStack
from functools import lru_cache, reduce
from operator import and_, attrgetter
from typing import Any, Iterable, Optional, Sequence, Union

from httpx import AsyncClient
from trio import run

from .candidate import Candidate, look
from .requirement import Information, Requirement

__all__ = ['Offreur']

Matches = Sequence[Candidate]


class Offreur:
    """Requirement and candidate provider for ResolveLib."""

    def __init__(self, repositories: Iterable[str]):
        self.exit_stack = AsyncExitStack()
        self.repositories = tuple(AsyncClient(base_url=url)
                                  for url in repositories)
        self.http = AsyncClient()  # generic HTTP client

    async def __aenter__(self) -> Offreur:
        for repository in self.repositories:
            await self.exit_stack.enter_async_context(repository)
        await self.exit_stack.enter_async_context(self.http)
        return self

    async def __aexit__(self, *exc_details: Any) -> None:
        await self.exit_stack.aclose()

    def __enter__(self) -> Offreur: return run(self.__aenter__)

    def __exit__(self, *exc_details: Any) -> None:
        run(self.__aexit__, *exc_details)  # as long as it works

    @lru_cache(maxsize=None)
    def get_candidates(self, project: str) -> Sequence[Candidate]:
        """Return all candidates for the given project."""
        return run(look, project, self.repositories)

    # Quack, quack, quack!

    def identify(self, candirement: Union[Candidate, Requirement]) -> str:
        """Return the identifier of the given candidate or requirement."""
        return candirement.name

    def get_preference(self, resolution: Optional[Candidate],
                       candidates: Iterable[Candidate],
                       information: Sequence[Information]) -> int:
        """Return a sort key for given requirement based on preference."""
        return 42

    def find_matches(self, requirements: Sequence[Requirement]) -> Matches:
        """Return all candidates satisfying the given requirements.

        - For VCS, local, and archive requirements,
          return the one-and-only match.
        - For *named* requirements, find concrete candidates
          from the repositories.

        The given requirements are of the same identifier
        and has at least one requirement.  The returned candidates
        are ordered by preference.
        """
        project = self.identify(requirements[0])
        specifier = reduce(and_, map(attrgetter('specifier'), requirements))
        return [candidate for candidate in self.get_candidates(project)
                if candidate.version in specifier]

    def is_satisfied_by(self, requirement: Requirement,
                        candidate: Candidate) -> bool:
        """Return if the given candidate satisfies requirement."""
        return candidate.version in requirement.specifier

    def get_dependencies(self, candidate: Candidate) -> Sequence[Requirement]:
        """Return the dependencies of the given candidate."""
        return []  # TODO
