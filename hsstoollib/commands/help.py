from hsstoollib.commands import Command
from hsstoollib.exceptions import *

class Help(Command):
   """
   The help command 
   """
   def addOptionsForCommand(self, parser):
      parser.add_argument('-a', '--all', action='store_true',
                          help='Print all available commands')
      parser.add_argument('-m', '--man', action='store_true',
                          help='Show man page for the command')

   def applyCommand(self):
      if self.options.all:
         self.printExtendedHelp()
      elif self.options.man or self.options.help:
         self.showDocumentation()
      else:
         self.printHelp()

      return True

   def printExtendedHelp(self):
      print "Extended help contains all the commands"

   def printHelp(self):
      print "Regular help contains the most used commands"
