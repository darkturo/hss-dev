""" 
This module will contain all the the exceptions that the hss-dev-tool can
raise.
"""

class BaseCommandLineException(Exception):
   """
   Base Exception for CommandLine errors.
   """
   def __init__(self, msg):
      if msg:
         self.msg = msg
      else:
         self.msg = ""

   def __str__(self):
      return self.msg.rstrip()

class CommandLineError(BaseCommandLineException):
   """
   When the user makes a mistake (this is most likely because he ordered a
   undefined command or the options provided are not valid according to
   argparse), this exception will be raised
   """
   pass

class CommandLineMisspelledError(BaseCommandLineException):
   """
   When the user makes a mistake (wrong command), but there is high
   probablity that it was because a misspelling, this exception will be
   raised
   """
   pass

class ExitWithSuccessException(BaseCommandLineException):
   """
   Whenever argparse decides to exit (with success), it is convenient to
   capture the output and let the main program handle that situation. In order
   to do that, if you're using RootArgumentParser, it will just raise an
   exception of this type
   """
   pass

class ExitWithErrorException(BaseCommandLineException):
   """
   Whenever argparse decides to exit (with an error), it is convenient to
   capture the output and let the main program handle that situation. In order
   to do that, if you're using RootArgumentParser, it will just raise an
   exception of this type.
   """
   pass
