"""
CommandLineParser provides a customised argparse.ArgumentParser.
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
      """
      Override ArgumentParser.exit(), to Raise an exception with either
      ExitWithSuccessException or ExitWithErrorException instead of printing
      'message' and calling os.sys.exit(status).
      This can be used to give better control of the execution flow. It comes
      quite handy for testing too.
      """
      if status != 0:
         errorMessage = ""
         if message:
            errorMessage = message.rstrip()
         errorMessage += " - [status = " + str(status) + " ]"
         raise ExitWithErrorException(errorMessage)
      else:
         raise ExitWithSuccessException(message)

   def format_help(self):
      """
      Override ArgumentParser.format_help() to provide a customized help output
      without the list of optional and positional arguments that comes by
      default with argparse.
      """
      formatter = self._get_formatter()

      # usage
      formatter.add_usage(self.usage, self._actions,
                          self._mutually_exclusive_groups)

      # description
      formatter.add_text(self.description)

      # positionals, optionals and user-defined groups
      for action_group in self._action_groups:
         if action_group.title == self._optionals.title:
            formatter._indent()
            formatter._indent()
            formatter.add_text(action_group.description)
            formatter.add_arguments(action_group._group_actions)

      # epilog
      formatter.add_text(self.epilog)

      # determine help from format above
      return formatter.format_help()
