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

import os
import random
from argparse import ArgumentParser
from datetime import datetime
from datetime import timedelta
from ..helper import get_state, set_state

random_range = [600, 3600]


def add_arguments(parser: ArgumentParser):
    parser.add_argument('--message', metavar='string', required=True, help='commit message')


def execute(state_file, args):
    dt = datetime.strptime(get_state(state_file, 'last_commit'), '%Y-%m-%d %H:%M:%S')

    random.seed()
    delta = timedelta(seconds=random.randint(random_range[0], random_range[1]))

    dt = dt + delta

    command = 'git commit -m "' + args.message + '" --date ' + dt.strftime('%Y-%m-%dT%H:%M:%S+0800')
    set_state(state_file, 'last_commit', dt.strftime('%Y-%m-%d %H:%M:%S'))
    os.system(command)
