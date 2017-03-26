#!/usr/bin/env python3
# OR-Lab is a package to automate experiment data collection and instrument calibration.
# Copyright (C) 2017  OpsResearch LLC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# No services should be using the serial port, for example getty.
# You may need to execute this with superuser privilege.
#

import sys
import re

if len(sys.argv) < 3:
   print("Usage: " + sys.argv[0] + " <input-log> <output-csv>")
   exit()

with open(sys.argv[1], 'r') as inFile:
	with open(sys.argv[2], 'w') as outFile:
		outFile.write("timestamp,v0,v1,v2,v3,v4,v5,v6,v7\n")
		timestamp = ''
		for line in inFile.readlines():
			line = line.strip()
			if line[:2] == '20':
				timestamp = line
			elif line[0] == '>':
				values = re.sub(r'\+', ',+', line[1:])
				values = re.sub(r'\-', ',-', values)
				outFile.write('"' + timestamp + '"' + values + '\n')



