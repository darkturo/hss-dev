from hsstoollib.commands import Command
from hsstoollib.exceptions import *

from hsstoollib.cluster import Clusters

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
