#!/usr/bin/env python3
#
# Copyright (C) 2018 VyOS maintainers and contributors
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 or later as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import time
import argparse

import tabulate

import vyos.keepalived
import vyos.util


def print_summary():
    vyos.keepalived.force_json_dump()
    json_data = vyos.keepalived.get_json_data()

    groups = []
    for group in json_data:
        data = group["data"]

        name = data["iname"]

        ltrans_timestamp = float(data["last_transition"])
        ltrans_time = vyos.util.seconds_to_human(int(time.time() - ltrans_timestamp))

        interface = data["ifp_ifname"]
        vrid = data["vrid"]

        row = [name, interface, vrid, ltrans_time]
        groups.append(row)

    headers = ["Name", "Interface", "VRID", "Last Transition"]
    output = tabulate.tabulate(groups, headers)
    print(output)

def print_statistics():
    vyos.keepalived.force_stats_dump()
    output = vyos.keepalived.get_statistics()
    print(output)


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-s", "--summary", action="store_true", help="Print VRRP summary")
group.add_argument("-t", "--statistics", action="store_true", help="Print VRRP statistics")

args = parser.parse_args()

if args.summary:
    print_summary()
elif args.statistics:
    print_statistics()
else:
    parser.print_help()
    sys.exit(1)
