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

   def test_error_when_aliases_is_not_a_list(self):
      """
      Testing an issue that occurs when I passed a string without a list.
      In particular the problem is:

         Given Help a subclass of Command, which id is "help", and it only has
         one alias as "--help", which by mistake has been provided using the
         string alone, instead of a list that contains the string.
         Withi this
            "help" matches as expected,
            "--help" matches too because of the alias,
            but also "-h" matches, which should not be the case.
      """
      _pathname = "/foo/bar/dtool"
      _somecommand = "help"
      _itsaliases  = "--help"
      cmd = DummyCommand(_somecommand, _itsaliases)

      # Match "help" with "help"
      self.assertTrue( cmd.match([_pathname, "help"]) );

      # Match "--help" with "--help" (because of the alias)
      self.assertTrue( cmd.match([_pathname, "--help"]) );

      # Try to match -h with --help, this should not match.
      self.assertFalse( cmd.match([_pathname, "-h"]) );

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
            return True
      cmd = List(_list, _aliases)
      self.assertEqual( cmd.options, () )
      self.assertTrue( cmd.apply( myArgv ) )
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
            return True
      cmd = List(_list, _aliases)
      self.assertEqual( cmd.options, () )
      self.assertTrue( cmd.apply( myArgv ) )
      self.assertTrue( cmd.options.verbose )
      self.assertFalse( cmd.options.quiet )

   def test_basic_behavior_apply_should_return_False_when_applyCommand_fails(self):
      """ Testing that when applyCommand fails, the error is propagated properly
      """
      _pathname = "/foo/bar/dtool"
      _list     = "list"
      _ls       = "ls"
      _aliases  = [_ls, "lst"]
      myArgv    = [_pathname, _ls, "--verbose", "--dry-run"]
      class List(Command):
         def applyCommand(self):
            return False
      cmd = List(_list, _aliases)
      self.assertEqual( cmd.options, () )
      self.assertFalse( cmd.apply( myArgv ) )
