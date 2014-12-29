import unittest
from command import Command

class DummyCommand(Command):
   pass

class TestCommandApply(unittest.TestCase):
   def test_apply_raises_NotImplementedError_when_used_directly(self):
      """ Test that apply raises a NotImplementedError Exception when calling it from an instance of the Command class """
      _pathname = "/foo/bar/devtool"
      _list     = "list"
      myArgv    = [_pathname, _list, "--help"] 
      cmd = Command(_list)
      with self.assertRaises(NotImplementedError):
         cmd.apply(myArgv) 

   def test_apply_raises_NotImplementedError_when_subclass_does_not_implements_apply(self):
      """ Test that apply raises a NotImplementedError Exception if the Command subclass does not implement the method """
      _pathname = "/foo/bar/devtool"
      _list     = "list"
      myArgv    = [_pathname, _list, "--help"] 
      cmd = DummyCommand(_list)
      with self.assertRaises(NotImplementedError):
         cmd.apply(myArgv) 

""" Test that the apply method from the Command subclass is called correctly"""
