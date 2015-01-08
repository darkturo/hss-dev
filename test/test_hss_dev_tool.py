import unittest
from command import Command
import hss

class DummyCommand(Command):
   pass

class TestDevTool(unittest.TestCase):
   """ Test basic tool functionality """
   def test_basic_command_matching(self):
      """ 
      Testing command matching
      Invocation with one command that matches with any of the provisioned commands should pass
      """
      _program = "devtool"
      _list = "list"
      _show = "show"
      _command = _list

      def myCommands():
         return [ DummyCommand(_list), DummyCommand(_show) ]

      self.assertTrue( hss.processCommandLine( myCommands, [ _program, _command ] ) )

# Backlog
# - invocation with one command that matches with the alias command should pass
# - invocation with two defined commands should return an error
# - invocation with one misspelled command that barely matches with either the command or the alias should fail
# - invocation with one misspelled command that is ambigous and matches with more than one provisioned command should fail
# - invocation with version should give the version
# - invocation with help, should give help
