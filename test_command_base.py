import unittest
from command import Command

class TestCommandBase(unittest.TestCase):
   def test_create_command(self):
      _list = "list"
      cmd = Command(_list)
      self.assertEqual(cmd.command, _list);

