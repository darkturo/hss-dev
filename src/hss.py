#!/usr/bin/python
import os
import difflib
import argparse
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

class Status(Command):
   pass

class CommandLineError(Exception):
   def __init__(self, msg):
      self.msg = msg

   def __str__(self):
      return self.msg

class CommandLineMisspelledError(Exception):
   def __init__(self, msg):
      self.msg = msg

   def __str__(self):
      return self.msg

class RootArgumentParser(argparse.ArgumentParser):
   def exit(self, status=0, message=None):
      errorMessage = ""
      if message:
         errorMessage = message
      errorMessage += " - [status = " + status + " ]"
      raise CommandLineError(errorMessage)

def buildCommandList():
   commandList = [ Status("status") ]
   return commandList

def buildRootArgumentParser(programName):
   return RootArgumentParser(programName, version='0.0.1');

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
   rootParser = buildRootArgumentParser(args[0])

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
         hint = "'{0}' is not a valid command. See '{1} --help'.\n\n".format(args[1], args[0])
         hint += "Did you mean one of these?\n"
         hint += "\n".join(bestMatches)
         raise CommandLineMisspelledError(hint)
      else:
         # Otherwise, the command is simply not supported, return False.
         return False
   else:
      # Use the rootParser to evaluate the provided arguments.
      opts = rootParser.parse_args(args)

   return False

if __name__ == "__main__":
   processCommandLine( buildCommandList(), os.sys.argv )
