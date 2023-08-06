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
import tempfile
from datetime import timedelta
from datetime import datetime
from argparse import ArgumentParser


def amend_commit(src_repo, dest_repo, commit, pre_cmd):
    os.chdir(src_repo)
    diff_file = "%s/gcm_diff" % (tempfile.gettempdir())
    os.system("git show --binary %s > %s" % (commit["id"], diff_file))

    if pre_cmd != "":
        pre_cmd = pre_cmd.replace("'", "\\'")
        os.system(pre_cmd.replace("{}", "'" + diff_file + "'"))

    os.chdir(dest_repo)
    msg = "".join(commit["comment"])
    os.system("git apply --index --binary %s/gcm_diff" % (tempfile.gettempdir()))
    os.system("git add .")
    os.system("git commit --message='%s' --date='%s'" % (msg.replace("'", "\\'"), commit["date"]))


def add_arguments(parser: ArgumentParser):
    parser.add_argument('--log', metavar='string', required=True, help='path name of log file')
    parser.add_argument('--execute', metavar='string', required=False, help='execute command before each commit')
    parser.add_argument('--offset', metavar='string', required=False, help='time offset of each commit')
    parser.add_argument('src_repo')
    parser.add_argument('dest_repo')


def execute(state_file, args):
    for ln in reversed(args.log.readlines()):
        ln = ln.strip()

        if ln == "":
            continue

        fd = ln.split("\t")

        if args.offset is None:
            offset = 0
        else:
            if args.offset[-1] == 's':
                offset = args.offset[:-1]
            elif args.offset[-1] == 'm':
                offset = int(args.offset[:-1]) * 60
            elif args.offset[-1] == 'h':
                offset = int(args.offset[:-1]) * 60 * 60
            elif args.offset[-1] == 'd':
                offset = int(args.offset[:-1]) * 60 * 60 * 24

        td = timedelta(seconds=offset)

        dt = datetime.strptime(fd[1][:-3] + fd[1][-2:], '%Y-%m-%dT%H:%M:%S%z') + td

        dts = dt.strftime("%Y-%m-%dT%H:%M:%S%z")

        commit = {
            "id": fd[0],
            "date": dts[:-2] + ':' + dts[-2:],
            "comment": eval(fd[2])
        }

        amend_commit(args.src_repo, args.dest_repo, commit, args.execute)
    return 0
