import unittest
from command import Command

class DummyCommand(Command):
   pass

class TestCommandApply(unittest.TestCase):
   def test_argv1_matches_with_cmd(self):
      """ Test that apply raises a NotImplementedError Exception when calling it from an instance of the Command class """
      _pathname = "/foo/bar/devtool"
      _list     = "list"
      myArgv    = [_pathname, _list, "--help"] 
      cmd = Command(_list)
      with self.assertRaises(NotImplementedError):
         cmd.apply(myArgv) 

""" Test that apply raises a NotImplementedError Exception if the Command subclass does not implemen the method """
""" Test that the apply method from the Command subclass is called correctly"""
