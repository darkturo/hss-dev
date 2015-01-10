import unittest
from hsstoollib.commands import Command

class DummyCommand(Command):
   pass

class TestCommandBaseClass(unittest.TestCase):
   """ Test basic things with the constructor """
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

class TestCommandMatch(unittest.TestCase):
   def test_argv_with_no_arguments(self):
      """ Testing the case when the command is called without any argument. 
          In this case myArgv will only contain the program_name. """
      _pathname = "/foo/bar/dtool"
      _list     = "list"
      myArgv    = [_pathname] 
      cmd = DummyCommand(_list)
      self.assertFalse( cmd.match(myArgv) );

   def test_argv1_matches_with_cmd(self):
      """ Testing that the command in argv[1]('list) matches with Command('list') """
      _pathname = "/foo/bar/dtool"
      _list     = "list"
      myArgv    = [_pathname, _list, "--help"] 
      cmd = DummyCommand(_list)
      self.assertTrue( cmd.match(myArgv) );

   def test_argv1_does_not_match_with_cmd(self):
      """ Testing that the command in argv[1]('show') does not match with Command('list') """
      _pathname = "/foo/bar/dtool"
      _list     = "list"
      myArgv    = [_pathname, "show"] 
      cmd = DummyCommand(_list)
      self.assertFalse( cmd.match(myArgv) );

   def test_argv1_does_not_match_with_cmd_but_matches_with_aliases_cmd(self):
      """ Testing that the alias command in argv[1]('ls') matches with some the aliases cmds of Command('list', ['ls', 'lst']) """
      _pathname = "/foo/bar/dtool"
      _list     = "list"
      _ls       = "ls"
      _aliases  = [_ls, "lst"]
      myArgv    = [_pathname, _ls, "--help"] 
      cmd = DummyCommand(_list, _aliases)
      self.assertTrue( cmd.match(myArgv) );

   def test_argv1_does_not_match_with_cmd_neither_aliases(self):
      """ Testing that the alias command in argv[1]('show') does not match with neither the command or the aliases commands of Command('list', ['ls', 'lst']) """
      _pathname = "/foo/bar/dtool"
      _list     = "list"
      _ls       = "ls"
      _aliases  = [_ls, "lst"]
      myArgv    = [_pathname, _ls, "--help"] 
      cmd = DummyCommand(_list, _aliases)
      self.assertTrue( cmd.match(myArgv) );

   def test_get_command_assocated_strings(self):
      """ 
      Testing that Command is capable of returning a list of the command name and aliases
      """
      _pathname = "/foo/bar/dtool"
      _list     = "list"
      _ls       = "ls"
      _lst      = "lst"
      _listing  = "listing"
      _aliases  = [_ls, _lst, _listing]
      cmd = DummyCommand(_list, _aliases)
      self.assertEqual( cmd.getCommandAssociatedStrings(), [_list] + _aliases )

   def test_basic_behavior_with_dummy_applyCommandImpl(self):
      """ Testing if the subclass provides a no implemented for addOptionsForCommand, three options are added by default.
      """
      _pathname = "/foo/bar/dtool"
      _list     = "list"
      _ls       = "ls"
      _aliases  = [_ls, "lst"]
      myArgv    = [_pathname, _ls] 
      class List(Command):
         def applyCommand(self):
            pass
      cmd = List(_list, _aliases)
      self.assertEqual( cmd.options, () )
      cmd.apply( myArgv )
      self.assertFalse( cmd.options.verbose )
      self.assertFalse( cmd.options.quiet )
      self.assertFalse( cmd.options.dry_run )

   def test_basic_behavior_with_dummy_applyCommandImpl_with_some_options(self):
      """ Testing if the subclass provides a no implemented for addOptionsForCommand, three options are added by default.
      """
      _pathname = "/foo/bar/dtool"
      _list     = "list"
      _ls       = "ls"
      _aliases  = [_ls, "lst"]
      myArgv    = [_pathname, _ls, "--verbose", "--dry-run"] 
      class List(Command):
         def applyCommand(self):
            pass
      cmd = List(_list, _aliases)
      self.assertEqual( cmd.options, () )
      cmd.apply( myArgv )
      self.assertTrue( cmd.options.verbose )
      self.assertFalse( cmd.options.quiet )
      self.assertTrue( cmd.options.dry_run )
