class MisspelledCommandException(Exception):
   pass

class Command:
   def __init__(self, command, aliases = []):
      """
      Command("the_command", ["thecmd", "cmd", "alias2"])
      """
      self.command = command
      self.aliases = aliases
   
   def match(self, args):
      """ Tells whether the command encoded in the argv[1] matches with the
          current value of self.command, or any of the aliases in the
          self.aliases list.
          If none of the previous gives a match, the method will find how close
          the command in argv[1] is to self.command (not to the aliases), and
          if it is 85% close to the command (some misspelling perhaps), match
          will raise a MisspelledCommandException.
      """
      inCommand = args[1]
      
      return ( inCommand == self.command or 
               inCommand in self.aliases )
