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
import getopt

# defaul program options
test=''
device=''
cmd =''
file=''
cnt = 1
delay = 0
regex=''
ifile=''
ofile=''
ts=False

# default serial port parameters
dev = device
baudrate = 9600
bytesize = serial.EIGHTBITS
parity = serial.PARITY_NONE
stopbits = serial.STOPBITS_ONE
timeout = 1.0
xonxoff = False
rtscts = True
dsrdtr = True

#
# MAIN LOOP
#
def main():

   ### Configure the serial port
   port = serial.Serial(
      port = dev,
      baudrate = baudrate,
      bytesize = bytesize,
      parity = parity,
      stopbits = stopbits,
      timeout = timeout,
      xonxoff = xonxoff,
      rtscts = rtscts,
      dsrdtr = dsrdtr
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


#
# PRINT USAGE
#
def usage():
   print(
"""
Usage:   run-cmds.py [options] <serial-device>

         Send a set of commands to a serial port and print the results.
         By default the command set is taken from stdin and the result set is written to stdout.

Options
         -in <file>
               Read the command set from <file>.

         -out <file>
               Read the command set from <file>.

         -regex <regex>
               The regular expression is applied to the result before it is output.


         -ts   A timestamp is prepended to each incoming result.

         -t  <result>
               Test a command set. Do not send the commands to the serial and set all results to <result>.

         -n <count> 
               Run the command set <count> times.

         -d <delay> 
               Delay bewteen command sets <delay> seconds.
""")
   sys.exit()

#
# GET OPTIONS
#
def getopts(argv):
   return

#
# ENTRY POINT
#
getopts(sys.argv)
main()




