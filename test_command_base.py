import unittest
from command import Command

class TestCommandBase(unittest.TestCase):
   def test_create_command(self):
      _list = "list"
      cmd = Command(_list)
      self.assertEqual(cmd.command, _list);

   def test_create_command_with_aliases(self):
      _list    = "list"
      _aliases = ["ls", "lst"]
      cmd = Command(_list, _aliases)
      self.assertEqual(cmd.aliases, _aliases);
