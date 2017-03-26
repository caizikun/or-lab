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

#
# No services should be using the serial port, for example getty.
# You may need to execute this with superuser privilege.
#

import sys
import serial

if len(sys.argv) < 2:
   print("Usage: " + sys.argv[0] + " <serial-device> [FLOW-CONTROL]")
   exit()

device = sys.argv[1]

flowCtrl = False
if len(sys.argv) >= 3:
   flowCtrl = True

port = serial.Serial(
   port=device,
   baudrate=9600,
   bytesize=serial.EIGHTBITS,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   timeout=1.0,
   xonxoff=False,
   rtscts=flowCtrl,
   dsrdtr=flowCtrl
 )    

if not port.isOpen():
   print("FAILED - Could not open port: " + device)
   exit()

port.flushInput()
port.flushOutput()

msg = bytes("Hello World!", 'UTF-8')
port.write(msg)

rsp = port.read(len(msg))
if len(rsp) == len(msg):
   print(rsp.decode('UTF-8'))
else:
   print("FAILED - Failed to receive a response: " + device)



