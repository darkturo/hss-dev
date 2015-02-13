import time
from hsstoollib.commands import Command
from hsstoollib.exceptions import *

from hsstoollib.cluster import getCluster

class Cpuloads(Command):
   """
   The Cpuloads command 
   """
   def addOptionsForCommand(self, parser):
      parser.add_argument('-c', '--cname', default="DefaultCluster",
            help='The cluster to query, default: DefaultCluster')
      parser.add_argument('-p', '--poll-rate', default=1000, type=int,
            help='The polling rate given in milliseconds, default: 1000ms')

   def applyCommand(self):
      cluster = getCluster (self.options.cname)
     
      if not cluster:
         return False

      load_category = "Normal"

      keys = sorted(cluster.getProcessorsOfType ("dicos"))
      tps = []
      for name in keys:
         tps.append (cluster.processors[name])

      try:
         while True:
            loads = []
            for tp in tps:
               loads.append (tp.load[load_category])

            print " ".join ('%.1f' % round(load, 1) for load in loads)
            time.sleep (self.options.poll_rate/1000)
      except KeyboardInterrupt:
         pass

      return True

