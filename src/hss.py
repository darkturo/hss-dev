#!/usr/bin/python
import os
from command import Command

#TODO: remove this comment 
##commandList = [ Status("status"),
##                Checkout("checkout"),
##                Config("config"),
##                Compile("compile"),
##                Deploy("deploy"),
##                Run("run"),
##                Stop("stop"),
##                GenUpgrade("gen-upgrade"),
##                ApplyUpgrade("apply-upgrade") ]
#for command in commandList:
#   if command.match(os.sys.argv):
#      try:
#         command.apply(os.sys.argv)
#      except Exception:
#         # Pokemon! catch 'em all!
#         os.sys.exit(1)
#      os.sys.exit(0)
#

class Status(Command):
   pass

def buildCommandList():
   commandList = [ Status("status") ]
   return commandList

def processCommandLine(commandList, args):
   return True

if __name__ == "__main__":
   processCommandLine( buildCommandList, os.sys.argv )
