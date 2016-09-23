from commands import Command, get_commands, get_command

class HelpCommand(Command):
  """help [command] -- built in help for the DoomRL server.

  With no arguments, list all commands. With a command specified, shows detailed
  help for that command."""

  nargs = 1

  def run(self, cmd):
    from inspect import getdoc

    if not cmd:
      for cmd in get_commands():
        print(getdoc(get_command(cmd)).split('\n')[0])
      return

    if not get_command(cmd):
      print('No such command. Try "help" for a list of all commands.')
    else:
      print(getdoc(get_command(cmd)))

