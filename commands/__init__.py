commands = {}

class CommandRegistration(type):
  def __new__(cls, clsname, bases, attrs):
    global commands
    newclass = super().__new__(cls, clsname, bases, attrs)
    name = clsname.replace('Command', '').lower()
    if name:
      commands[name] = newclass()
    return newclass

class Command(object, metaclass=CommandRegistration):
  nargs = 0
  def run(self, *args):
    return 'Not implemented yet.'

def argsplit(string, max=2):
  args = string.split(maxsplit=max-1)
  while len(args) < max:
    args.append('')
  return args

def run_command(cmd, args):
  if not cmd in commands:
    print('Unrecognized command: %s' % cmd)
    return

  result = commands[cmd].run(*argsplit(args, max=commands[cmd].nargs))
  if result:
    print('Error: %s' % result)

def get_commands():
  return commands

def get_command(cmd):
  return commands.get(cmd)

# Import all of the commands so that they get registered.
from commands import config, delete, help, login, mortem, play, rebuild, register, replay, scores, watch
