from hsstoollib.commands import Command
from hsstoollib.exceptions import *

from hsstoollib.cluster import Clusters

class TPs(Command):
   """
   The TPs command 
   """
   def addOptionsForCommand(self, parser):
      parser.add_argument('-c', '--cname', default="DefaultCluster",
                          help='The cluster to query.')

   def applyCommand(self):
      clusters = Clusters()
      try:
         cluster = clusters[self.options.cname]
         for tp in sorted(cluster.processors.keys()):
            print tp,
      except KeyError:
         print "Cluster %s is not running." % self.options.cname
         return False

      return True

   def printExtendedHelp(self):
      print "Extended help contains all the commands"

   def printHelp(self):
      print "Regular help contains the most used commands for TPs"
