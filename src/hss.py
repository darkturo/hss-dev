#!/usr/bin/python
import os
from command import Command

#commandList = [ Status("status"),
#                Checkout("checkout"),
#                Config("config"),
#                Compile("compile"),
#                Deploy("deploy"),
#                Run("run"),
#                Stop("stop"),
#                GenUpgrade("gen-upgrade"),
#                ApplyUpgrade("apply-upgrade") ]
class Status(Command):
   pass

commandList = [ Status("status") ]
for command in commandList:
   if command.match(os.sys.argv):
      try:
         command.apply(os.sys.argv)
      except Exception:
         # Pokemon! catch 'em all!
         os.sys.exit(1)
      os.sys.exit(0)
