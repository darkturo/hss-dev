from hsstoollib.commands import Command
from hsstoollib.exceptions import *

from hsstoollib.cluster import getCluster

import time

class Counters(Command):
   """
   The Counters command 
   """
   def addOptionsForCommand(self, parser):
      parser.add_argument('-c', '--cname', default="DefaultCluster",
                          help='The cluster to query.')
      parser.add_argument('-f', '--follow', action='store_true',
                          help='Monitor the counters, print them as they are increased.')

   def applyCommand(self):
      cluster = getCluster (self.options.cname)
     
      if not cluster:
         return False

      if not self.options.follow:
         print cluster.counters
      else:
         try:
            previous = cluster.counters
            while True:
               new = cluster.counters
               compareCounters (previous, new)
               previous = new
         except KeyboardInterrupt:
            pass


      return True

   def printExtendedHelp(self):
      print "Extended help contains all the commands"

   def printHelp(self):
      print "Regular help contains the most used commands for TPs"


def compareCounters (previous, new):
   for counter in new.itervalues():
      for valueName, newValue in counter.iteritems():
         state = None
         if not counter.name in previous:
            # We have found a new counter
            state = "new counter"
         elif not valueName in previous[counter.name]:
            # We have found a new value
            state = "new value"
         else:
            # We already have an old value
            oldValue = previous[counter.name][valueName]
            if oldValue != newValue:
               state = "changed from %s" % oldValue
         
         # If it's state changed, print it!
         if state:
            print "(%s) %s/%s %s: current value=%s" % (time.strftime("%X"), counter.job, counter.name, state, newValue)

