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
      parser.add_argument('-1', '--once', action='store_true',
                          help='Compare counters only once.')

   def applyCommand(self):
      cluster = getCluster (self.options.cname)
     
      if not cluster:
         return False

      if self.options.follow:
         try:
            previous = cluster.counters
            print "Starting measurements."
            while True:
               new = cluster.counters
               compareCounters (previous, new)
               previous = new
         except KeyboardInterrupt:
            pass
      elif self.options.once:
         print "Collecting counters, wait a moment..."
         first = cluster.counters
         try:
            print "Ready. Use Ctrl-C to make comparison."
            # Wait for interrupt
            while True:
               time.sleep(10)
         except KeyboardInterrupt:
            print "Collecting counters, wait a moment..."
            second = cluster.counters
            compareCounters (first, second)
      else:
         print cluster.counters

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
            state = "new counter. Value=%s" % newValue
         elif not valueName in previous[counter.name]:
            # We have found a new value
            state = "new value. Value=%s" % newValue
         else:
            # We already have an old value
            oldValue = previous[counter.name][valueName]
            if oldValue != newValue:
               state = "changed %s->%s: " % (oldValue, newValue)
               diff = int(newValue) - int(oldValue)
               if diff >= 0:
                  state += "+"
               state += str(diff)
          
         # If it's state changed, print it!
         if state:
            print "(%s) %s: %s %s" % (time.strftime("%X"), counter.name, valueName, state)

