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

if len(sys.argv) < 3 or (len(sys.argv) >= 4 and sys.argv[3] != "LOOPBACK"):
   print("Usage: " + sys.argv[0] + " <serial-device> <module-address> [LOOPBACK]")
   exit()

device = sys.argv[1]
module = sys.argv[2]


if len(module) != 2:
   print("ERROR - The module address must be two hexadecimal characters!")
   exit()

### Loopback test mode
loopback = False
if len(sys.argv) >= 4 and sys.argv[3] == "LOOPBACK":
   loopback = True

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

### Enable calibration mode.
cmd = "~"+module+"1"
rsp = "!" + module
if loopback: rsp = cmd
cmdBytes = bytes(cmd, 'UTF-8')
rspBytes = bytes(rsp, 'UTF-8')

port.write(cmdBytes)
if port.read(len(rspBytes)) != rspBytes:
   print("ERROR - Could not enable calibration mode: " + device + ":" + module)
   exit()

### Zero calibration
print("Apply the ZERO calibration voltage to channel 0, then press enter.")
sys.stdin.readline()

cmd = "$"+module+"1"
rsp = "!" + module
if loopback: rsp = cmd
cmdBytes = bytes(cmd, 'UTF-8')
rspBytes = bytes(rsp, 'UTF-8')

port.write(cmdBytes)
if port.read(len(rspBytes)) != rspBytes:
   print("ERROR - Could not perform the zero calibration: " + device + ":" + module)
   exit()

### Full scale calibration
print("Apply the FULL SCALE calibration voltage to channel 0, then press enter.")
sys.stdin.readline()

cmd = "$"+module+"0"
rsp = "!" + module
if loopback: rsp = cmd
cmdBytes = bytes(cmd, 'UTF-8')
rspBytes = bytes(rsp, 'UTF-8')

port.write(cmdBytes)
if port.read(len(rspBytes)) != rspBytes:
   print("ERROR - Could not perform the full scale calibration: " + device + ":" + module)
   exit()

### Disable calibration mode.
cmd = "~"+module+"0"
rsp = "!" + module
if loopback: rsp = cmd
cmdBytes = bytes(cmd, 'UTF-8')
rspBytes = bytes(rsp, 'UTF-8')

port.write(cmdBytes)
if port.read(len(rspBytes)) != rspBytes:
   print("ERROR - Could not disable calibration mode: " + device + ":" + module)
   exit()

### Success
print("SUCCESS - This single calibration cycle is complete, repeat 6-7 times.")



