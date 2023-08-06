# Console script
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

from argparse import ArgumentParser
from os.path import basename
from sys import executable

from resolvelib import Resolver

from . import __version__
from .provider import Offreur
from .reporter import Reporter
from .requirement import Requirement

PYPI = 'https://pypi.org/simple'

if __name__ == '__main__':
    arg_parser = ArgumentParser(prog=f'{basename(executable)} -m offre',
                                epilog="Python, m'offre qqch!")
    arg_parser.add_argument('qqch', nargs='*', type=Requirement,
                            help='requirement specifiers')
    arg_parser.add_argument('-V', '--version', action='version',
                            version=f'offre {__version__}')
    arg_parser.add_argument('--repositories', nargs='*', default=[PYPI],
                            help=('base URLs of Python package repositories'
                                  ' to use, default to PyPI'),
                            metavar='URL')
    args = arg_parser.parse_args()

    with Offreur(args.repositories) as provider:
        resolver = Resolver(provider, Reporter())
        resolver.resolve(args.qqch)
