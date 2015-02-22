import time
import sys
from hsstoollib.commands import Command
from hsstoollib.exceptions import *

from hsstoollib.cluster import getCluster

class GetEnv (Command):
   """
   The GetEnv command
   """
   def addOptionsForCommand(self, parser):
      parser.add_argument('-c', '--cname', default="DefaultCluster",
            help='The cluster to query, default: DefaultCluster')
      parser.add_argument("variable",
            help="The variable to retrieve")

   def applyCommand(self):
      cluster = getCluster (self.options.cname)

      if not cluster:
         return False

      value = cluster.getEnvironmentVariable (self.options.variable)
      if value:
         print value
         return True
      else:
         print "No variable with name %s" % self.options.variable
         return False
