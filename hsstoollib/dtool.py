#!/usr/bin/python
import os
import difflib
import argparse
import hsstoollib
from hsstoollib.commands import *
from hsstoollib.exceptions import CommandLineError, CommandLineMisspelledError, ExitWithSuccessException, ExitWithErrorException

programName = "hss"

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

class Status(Command):
   pass

class RootArgumentParser(argparse.ArgumentParser):
   def exit(self, status=0, message=None):
      if status != 0:
         errorMessage = ""
         if message:
            errorMessage = message.rstrip()
         errorMessage += " - [status = " + str(status) + " ]"
         raise CommandLineError(errorMessage)
      else:
         raise ExitWithSuccessException(message)

def buildCommandList():
   commandList = [ Status("status") ]
   return commandList

def buildRootArgumentParser(programName):
   parser     = RootArgumentParser( programName );

   versionStr = "{0} version {1}".format(programName, hsstoollib.__version__)
   parser.add_argument('-v', '--version', action='version', version=versionStr)

   return parser

def processCommandLine(commandList, args):
   # Evaluate in chain whether any of the available commands in commandList
   # matches with the command line arguments (args), and apply the
   # corresponding command.
   for command in commandList:
      if command.match(args):
         command.apply(args)
         return True

   # If the command line command is not in commandList, giving some hints to
   # the user of what went wrong should be nice. For that we'll use an
   # instance of argparse.ArgumentParser which will print help as needed, and
   # give support for some basic options (i.e. --version or --help).
   rootParser = buildRootArgumentParser( programName )

   if len(args) <= 1:
      # User is clue-less here, give him the help print
      rootParser.print_help()
      return False

   if not args[1][0] == '-':
      # Find the closest alternatives to the given command. With this the tool
      # will determine if the user misspelled the command, and thus give him
      # better hints of what went wrong.
      possibleCommandNames = map(lambda c: c.getCommandAssociatedStrings(), commandList)
      bestMatches = difflib.get_close_matches(args[1], possibleCommandNames)

      if len(bestMatches) > 0:
         # If there is possible matches, the user may have misspelled the command
         hint = "'{0}' is not a valid command. See '{1} --help'.\n\n".format(args[1], programName)
         hint += "Did you mean one of these?\n"
         hint += "\n".join(bestMatches)
         raise CommandLineMisspelledError(hint)
      else:
         # Otherwise, the command is simply not supported, return False.
         return False
   else:
      # Use the rootParser to evaluate the provided arguments.
      try:
         opts = rootParser.parse_args(args)
      except ExitWithSuccessException as msg:
         print msg 
         return True

   return False

if __name__ == "__main__":
   processCommandLine( buildCommandList(), os.sys.argv )
