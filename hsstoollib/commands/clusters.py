from hsstoollib.commands import Command
from hsstoollib.exceptions import *

from hsstoollib.cluster import Clusters, getCluster

class RunningClusters(Command):
   """
   The TPs command
   """
   def addOptionsForCommand(self, parser):
      pass

   def applyCommand(self):
      clusters = Clusters()
      if clusters:
         for cluster in sorted(clusters.keys()):
            print cluster
      else:
         print "No clusters running."

      return True

   def printExtendedHelp(self):
      pass

   def printHelp(self):
      pass



class ShowCluster(Command):
   """
   The cluster show command
   """
   def addOptionsForCommand(self, parser):
      parser.add_argument('-c', '--cname', default="DefaultCluster",
                          help='The cluster to query.')

   def applyCommand(self):
      cluster = getCluster (self.options.cname)
     
      if not cluster:
         return False

      print cluster.describe ()
      return True
