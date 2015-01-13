# Arturo Escudero <arturo.escudero@ericsson.com> 2015
import argparse
import hsstoollib
from hsstoollib.misc.argparse_helpers import CommandLineParser

class Command:
   """
   Command Base class.

   Extend this command class in order to use it.

   The class provides the following methods:
      - match(argument_list)
         This method tell if the provided argument list
         (os.sys.argv alike) matches with the instance of
         Command.
      - apply(argument_list)
         This method, parses, and validates the argument_list
         using argparse. If the parsing is successful, the
         method will invoke the subclass method applyCommand,
         to trigger the required actions for the command the
         class represents.

   All the subclasses of Command need to implement the
   following methods in order to make it work properly with a
   collection of commands:
      - self.addOptionsForCommand(parser)
         This method should be overwritten in order to add more
         specific options for the command subclass.
      - applyCommand()
         This method needs to be implemented in the Command
         subclass. The purpose of this method is to execute
         the actions that the subclass of Command is meant to
         do.
         The method will be invoked if the parsing of the
         command line options was successful. These options
         will be saved in the self.options attribute, which
         contains an object which attributes are all the
         defined options, and their values depends on what
         the user provided from the command line.
   """
   def __init__(self, command, aliases = [], usage = None):
      """
      Constructor.

        Arguments:
         command - The name of the command to be used for the
                   parsing.
         aliases - A list of possible alias, that cannot be
                   derived from the name.
      """
      self._program = hsstoollib.__dtoolname__
      self.command = command

      if type(aliases) is str:
         self.aliases = [ aliases ]
      else:
         self.aliases = aliases

      if usage:
         self.usage = usage
      else:
         self.usage = "%(prog)s [-v | --verbose] [options]"

      self._parser = self.__buildArgumentParser()
      self.options = ()

   def __str__(self):
      return ",".join( self.getListOfCommandNames() )

   def getListOfCommandNames(self):
      """
      Returns a list with the identifier for the command and the list of
      defined aliases for the command.
      """
      return [ self.command ] + self.aliases

   def match(self, args):
      """
      Tells whether the command encoded in the argv[1]
      matches with the current value of self.command, or any
      of the aliases in the self.aliases list.
      """
      if (len(args) <= 1):
         return False

      inCommand = args[1]
      return ( inCommand == self.command or
               inCommand in self.aliases )

   def apply(self, args):
      """
      Applies the logic for the implementation of the
      particular command. In order to do this, the method
      will parse the command line arguments (using the
      default options -provisioned by __buildArgumentParser,
      plus some other options provided by the Command subclass
      via the addOptionsForCommand method), collect them into
      the class attribute self.options, and finally invoking
      the method applyCommand(), which should contain the
      proper implementation of the actions to be performed by
      the subclass.

      When its done, it will return True or false indicating whether the
      operation was executed successfully.
      """
      # Parse command line options, but remove the program name and the
      # command from the list using a slice of the args array.
      self.options = self._parser.parse_args(args[2:])

      # Show man pages (if exist) for the command
      if self.options.help:
         self.showDocumentation()
         return True

      # Call applyCommand to apply the program logic.
      return self.applyCommand()

   def addOptionsForCommand(self, parser):
      """
      Override this implementation in case you want to make your Command
      subclass to support extra options.

      The idea is to provide with this method new options by using the
      interface of the argparse.ArgumentParser class.

      For convenience, in case no extra options is needed, this will provide a
      basic impl. which will add no extra option.
      """
      pass

   def applyCommand(self):
      """
      Override this implementation to provide the logic of the Command subclass.

      This method will contain the logic for the set of actions the command
      represents. For that it will use self.options, as well as other data.

      Returns True/False to communicate the success or error of the involved
      operations.
      """
      raise NotImplementedError

   def showDocumentation(self):
      """
      Show documentation for the command using man.
      """
      raise NotImplementedError
#      help(self.__module__)
#      man = Manpage(name, version, author, argparse)
#      man.show()


   def __buildArgumentParser(self):
      """
      Build an argparse.ArgumentParser instance and default and user defined
      options for the command. 
      """
      prog = self._program + " " + self.command;
      parser = CommandLineParser( prog, 
                                  usage = self.usage,
                                  conflict_handler = 'resolve' )

      # Add default options to the ArgumentParser
      self.__addDefaultOptionsForCommand( parser )

      # Add user defined options to the ArgumentParser
      self.addOptionsForCommand( parser )

      return parser

   def __addDefaultOptionsForCommand(self, parser):
      """
      Add default options --verbose, --quiet and --dry-run to the parser.
      """
      # -- Adding help options
      # The option -h, will be handed over to the default argparse
      # autogenerated help (ation=help). 
      parser.add_argument('-h', action='help', 
                          help=argparse.SUPPRESS)
      # The option --help will be added as a flag into self.options, and
      # handled later in the Command.apply method.
      parser.add_argument('--help', action='store_true', 
                          help=argparse.SUPPRESS)
      # Both options are added automatically by argparse, but I'm
      # overwritting them here because I want to have a different behavior.
      # ------------

   
      # Add verbose and quiet mode options, which should not be enabled at
      # the same time.
      group = parser.add_mutually_exclusive_group()
      group.add_argument('-v', '--verbose', action='store_true',
                          help='Enable verbose mode')
      group.add_argument('-q', '--quiet', action='store_true',
                          help='Enable quiet mode')

      # TODO: not sure about the dry-run option by default now...
      # Add a default dry-run option
      parser.add_argument('-n', '--dry-run', action='store_true',
                          help='This option will print the actions that the ' +
                               'script is planning to do, but it will not '   +
                               'perform any real action');
