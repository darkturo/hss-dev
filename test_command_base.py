import unittest
from command import Command

class TestCommandBase(unittest.TestCase):
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

   def test_match_argv1_should_match_with_cmd(self):
      """ Testing that the command in argv[1] matches with Command('list') """
      _pathname = "/foo/bar/devtool"
      _list     = "list"
      myArgv    = [_list, "--help"] 
      cmd = Command(_list)
      self.assertTrue( cmd.match(myArgv) );
