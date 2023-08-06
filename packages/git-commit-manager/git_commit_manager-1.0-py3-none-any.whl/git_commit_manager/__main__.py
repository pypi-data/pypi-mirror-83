# -*- coding: utf-8 -*-
# Copyright (C) 2020 HE Yaowen <he.yaowen@hotmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import importlib
import argparse


def print_help():
    usage = '''usage: gcm <command> [parameters]
To see help text, you can run:
  gcm <command> --help
'''
    sys.stderr.write(usage)


def main():
    if len(sys.argv) < 2 or sys.argv[1][0] == '-':
        print_help()
        return -1

    parser = argparse.ArgumentParser()

    parser.add_argument('command')

    # add common arguments
    group = parser.add_argument_group('common')
    group.add_argument('--state', metavar='string', required=False, help='specific profile from your configurations',
                       default=os.getenv('HOME') + '/.gcm_state')

    command = importlib.import_module('git_commit_manager.command.%s' % (sys.argv[1].replace('-', '_')))
    command.add_arguments(parser)

    args = parser.parse_args()

    return command.execute(state_file=args.state, args=args)


if __name__ == '__main__':
    sys.exit(main())
