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
import time
import serial

if len(sys.argv) < 3:
   print("Usage: " + sys.argv[0] + " <serial-device> <cmd-string> [<count> [<delay>]]")
   exit()

device = sys.argv[1]
cmd = sys.argv[2]

cnt = 1
if len(sys.argv) >= 4:
   cnt = int(sys.argv[3])

delay = 0
if len(sys.argv) >= 5:
   delay = float(sys.argv[4]) 

### Configure the serial port
port = serial.Serial(
   port = device,
   baudrate = 9600,
   bytesize = serial.EIGHTBITS,
   parity = serial.PARITY_NONE,
   stopbits = serial.STOPBITS_ONE,
   timeout = 1.0,
   xonxoff = False,
   rtscts = True,
   dsrdtr = True
 )    

### Make sure the serial port open successfully
if not port.isOpen():
   print("ERROR - Could not open the serial device: " + device)
   exit()

### Empty the serial port buffers
port.flushInput()
port.flushOutput()

while cnt > 0:

   #write command
   port.write(bytes(cmd + "\r", 'UTF-8'))

   #read response
   buf = port.read()
   time.sleep(0.1)
   while port.inWaiting() > 0:
      buf += port.read()

   if len(buf) > 0:
      print(buf.decode('UTF-8'))
   else:
      print("ERROR - Failed to receive a response: " + device)

   time.sleep(delay)
   cnt -= 1

