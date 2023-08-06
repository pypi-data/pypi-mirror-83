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
import json
import time
from argparse import ArgumentParser


def add_arguments(parser: ArgumentParser):
    pass


def execute(state_file, args):
    if not os.path.exists(state_file):
        states = {"last_commit": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}
        json.dump(states, open(state_file, 'w'))
