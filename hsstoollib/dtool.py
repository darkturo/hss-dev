#!/usr/bin/python
import os
import difflib
import argparse
import hsstoollib
from hsstoollib.commands import *
from hsstoollib.misc import *
from hsstoollib.exceptions import CommandLineError, CommandLineMisspelledError, ExitWithSuccessException, ExitWithErrorException

programName = hsstoollib.__dtoolname__

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

def buildCommandList():
   """
   Returns a list with all the supported Commands that dtool can handle.
   """
   return [Help("help", "--help"), Status("status"),
           TPs("tps", aliases = ["processors"]),
           RunningClusters("clusters", aliases = ["running", "maias"]),
           ShowCluster("show", aliases = ["describe"]),
           Cpuloads("cpuloads", aliases = ["loads"])]

def buildRootArgumentParser(programName):
   """
   Creates an instance of CommandLineParser, with a set of options to generate
   a good an informative help text, and it adds basic options for the 'root'
   tool (dtool); for instance to handle the version or help printing.
   """
   usageText  = "%(prog)s [--version] [--help] <command> [<args>]"
   parser = CommandLineParser( prog = programName,
                               conflict_handler='resolve',
                               add_help = False,
                               usage = usageText );

   versionText = "{0} version {1}".format(programName, hsstoollib.__version__)
   parser.add_argument('-v', '--version', action='version', version=versionText)

   return parser

def processCommandLine(commandList, args):
   """
   This function takes a list of Command(s), and the command line argument,
   and proceeds first to find whether the command in the command line argument
   matches or not with any of the provided commandList. If so, it will just
   apply the action and return success.
   If there is no match, it tries to determine if it was a misspelling, in
   which case it will raise an exception with all the possible matches.
   If it determines there was not a misspelling, and the command is not an
   option (does not start with "-") then it will return False.
   Options are parsed using the rootParser, which is an instance of
   CommandLineParser.
   """
   rootParser = buildRootArgumentParser( programName )
   if len(args) <= 1:
      # User is clue-less here, give him the help print using the Help command
      args.append("help")

   # Evaluate in chain whether any of the available commands in commandList
   # matches with the command line arguments (args), and apply the
   # corresponding command.
   for command in commandList:
      if command.match(args):
         return command.apply(args)

   if not args[1][0] == '-':
      # Find the closest alternatives to the given command. With this the tool
      # will determine if the user misspelled the command, and thus give him
      # better hints of what went wrong.
      possibleCommandNames = map(lambda c: c.getListOfCommandNames(), commandList)
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
      # Finally, use the rootParser to evaluate the provided arguments.
      opts = rootParser.parse_args(args)

   return False

if __name__ == "__main__":
   result = False
   try:
      result = processCommandLine( buildCommandList(), os.sys.argv )
   except ExitWithSuccessException as msg:
      print msg 
   except ExitWithErrorException as errMsg:
      print str(errMsg).replace(os.sys.argv[0], "")

   if result:
      os.sys.exit( 0 )
   else:
      os.sys.exit( 1 )

