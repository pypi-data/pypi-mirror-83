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
from argparse import ArgumentParser


def get_commits(repo_dir):
    os.chdir(repo_dir)

    commits = []
    logs = os.popen("git log --date=iso-strict").readlines()

    for i in range(0, len(logs)):
        ln = logs[i].strip()

        if ln[0:6] == 'commit':
            commit = {
                "id": ln[7:],
                "comment": []
            }

            i += 1
            commit["author"] = logs[i].strip()[8:].strip()

            i += 1
            commit["date"] = logs[i].strip()[5:].strip()

            i += 1

            while i < len(logs) and logs[i][0:6] != "commit":
                comment = logs[i].strip()

                if comment != "":
                    commit["comment"].append(logs[i].strip())

                i += 1

            commits.append(commit)

    return commits


def add_arguments(parser: ArgumentParser):
    parser.add_argument('path')


def execute(state_file, args):
    for commit in get_commits(args.path):
        print("%s\t%s\t%s" % (commit['id'], commit['date'], commit['comment']))

    return 0
