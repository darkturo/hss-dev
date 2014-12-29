import unittest
from command import Command

class TestCommandBaseClass(unittest.TestCase):
   def test_create_command(self):
      """ Testing the constructor with one argument """
      _list = "list"
      cmd = Command(_list)
      self.assertEqual(cmd.command, _list);

   def test_create_command_with_aliases(self):
      """ Testing the constructor with two arguments (list and aliases)"""
      _list    = "list"
      _aliases = ["ls", "lst"]
      cmd = Command(_list, _aliases)
      self.assertEqual(cmd.aliases, _aliases);

