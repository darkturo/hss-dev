__description__ = """ 
   HSS Command(s) subclasses that has the knowledge on how to run, compile,
   deploy, test and run hss.  
   """

import argparse
from hsstoollib.exceptions import ExitWithSuccessException, ExitWithErrorException
class CommandLineParser(argparse.ArgumentParser):
   """
   This is just a simple subclass of argparse.ArgumentParser, which adapts
   the behavior of argparse to:
      - raise an exception instead of call os.sys.exit
   """
   def exit(self, status=0, message=None):
      if status != 0:
         errorMessage = ""
         if message:
            errorMessage = message.rstrip()
         errorMessage += " - [status = " + str(status) + " ]"
         raise ExitWithErrorException(errorMessage)
      else:
         raise ExitWithSuccessException(message)

"""
Explicit exports:
"""
from base import Command
__all__ = [ 
            'base', 
            'CommandLineParser',
            'Command'
          ]
