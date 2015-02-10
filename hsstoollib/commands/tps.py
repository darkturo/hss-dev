from hsstoollib.commands import Command
from hsstoollib.exceptions import *

from hsstoollib.cluster import getCluster

class TPs(Command):
   """
   The TPs command 
   """
   def addOptionsForCommand(self, parser):
      parser.add_argument('-c', '--cname', default="DefaultCluster",
                          help='The cluster to query.')

   def applyCommand(self):
      cluster = getCluster (self.options.cname)
     
      if not cluster:
         return False

      for tp in sorted(cluster.processors.keys()):
         print tp,

      return True

   def printExtendedHelp(self):
      print "Extended help contains all the commands"

   def printHelp(self):
      print "Regular help contains the most used commands for TPs"
