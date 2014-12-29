class Command:
   def __init__(self, command, aliases = []):
      """
      Command("the_command", ["thecmd", "cmd", "alias2"])
      """
      self.command = command
      self.aliases = aliases
