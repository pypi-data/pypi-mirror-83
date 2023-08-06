# Reporter for ResolveLib
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

from typing import Any, Optional

from packaging.requirements import Requirement

from .candidate import Candidate

__all__ = ['Reporter']


class Reporter:
    """Progress reporter for ResolveLib."""

    def starting(self) -> None:
        print('starting')

    def starting_round(self, index: int) -> None:
        print('starting round', index)

    def ending_round(self, index: int, state: Any) -> None:
        print(f'ending round {index}: {state}')

    def ending(self, state: Any) -> None:
        print('ending', state)

    def adding_requirement(self, requirement: Requirement,
                           parent: Optional[Candidate]) -> None:
        print('adding', requirement, 'from', parent)

    def backtracking(self, candidate: Candidate) -> None:
        print('backtracking', candidate)

    def pinning(self, candidate: Candidate) -> None:
        print('pinning', candidate)
