import unittest
from hsstoollib.commands import Command
import hsstoollib.dtool as dtool

class DummyCommand(Command):
   def applyCommand(self):
      pass

class TestDevTool(unittest.TestCase):
   """ Test basic tool functionality. """
   def test_basic_call_with_no_argument(self):
      """ 
      Testing behavior without any argument
      Simulating the case when the user invokes the devtool without any
      argument. When doing that, processCommandLine should return False.
      """
      _program = "dtool"
      _list = "list"
      _show = "show"
      def myCommandsBuilder():
         return [ DummyCommand(_list), DummyCommand(_show) ]

      self.assertFalse( dtool.processCommandLine( myCommandsBuilder(), [ _program ] ) )

   def test_basic_command_matching(self):
      """ 
      Testing command matching.
      Invocation with one command that matches with any of the provisioned commands should pass
      """
      _program = "dtool"
      _list = "list"
      _show = "show"
      _command = _list

      def myCommandsBuilder():
         return [ DummyCommand(_list), DummyCommand(_show) ]

      self.assertTrue( dtool.processCommandLine( myCommandsBuilder(), [ _program, _command ] ) )

   def test_command_matching_with_alias(self):
      """
      Testing command matching with alias.
      invocation with one command that matches with the alias command should pass
      """
      _program = "dtool"
      _list = "list"
      _list_aliases = ["ls", "l", "ll"]
      _show = "show"
      _command = "ll"

      def myCommandsBuilder():
         return [ DummyCommand(_list, _list_aliases), DummyCommand(_show) ]

      self.assertTrue( dtool.processCommandLine( myCommandsBuilder(), [ _program, _command ] ) )

   def test_command_not_matching(self):
      """
      Testing the case when there is no match.
      invocation with a command that does not match gives an error
      """
      _program = "dtool"
      _list = "list"
      _list_aliases = ["ls", "l", "ll"]
      _show = "show"
      _config = "config"
      _command = "status"

      def myCommandsBuilder():
         return [ DummyCommand(_list, _list_aliases), DummyCommand(_show), DummyCommand(_config) ]

      self.assertFalse( dtool.processCommandLine( myCommandsBuilder(), [ _program, _command ] ) )

   def test_version_option(self):
      """
      Testing --version option support
      invocation without a command but with the version option should give the version
      """
      _program = "dtool"
      _list = "list"
      _list_aliases = ["ls", "l", "ll"]
      _show = "show"
      _command = "-v"

      def myCommandsBuilder():
         return [ DummyCommand(_list, _list_aliases), DummyCommand(_show) ]

      self.assertTrue( dtool.processCommandLine( myCommandsBuilder(), [ _program, _command ] ) )

   def test_help_option(self):
      """
      Testing --help option support
      invocation without a command but with the help option should print help.
      """
      _program = "dtool"
      _list = "list"
      _list_aliases = ["ls", "l", "ll"]
      _show = "show"
      _command = "-h"

      def myCommandsBuilder():
         return [ DummyCommand(_list, _list_aliases), DummyCommand(_show) ]

      self.assertTrue( dtool.processCommandLine( myCommandsBuilder(), [ _program, _command ] ) )

# - invocation with help, should give help

# Backlog
# - invocation with one misspelled command that barely matches with either the command or the alias should fail
# - invocation with one misspelled command that is ambigous and matches with more than one provisioned command should fail
# - invocation with two defined commands should return an error
# - invocation with a correct commands but not supported options should Fail.
