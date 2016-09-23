import doomrl
import os
import shutil
import subprocess

from commands import Command

class ConfigCommand(Command):
  """config <file> [reset] -- edit or reset configuration files

  As "config <file>", lets you edit one of your DoomRL configuration files.
  As "config <file> reset", lets you reset a file to defaults.
  As "config all reset", resets all files to defaults.

  Available files are:

    controls -- keyboard controls
    colours  -- game display colours
    user     -- user settings and general configuration

  Note that DoomRL has options not listed in any of these files; these options
  are overriden by the server and adding them yourself will have no effect.
  """

  nargs = 2

  def run(self, file, reset):
    if not doomrl.user():
      return 'You must be logged in.'

    if reset and reset != 'reset':
      return 'Invalid second argument. See "help config".'

    files = frozenset(['controls', 'colours', 'user'])

    if reset and file == "all":
      print("Restoring default configuration files.")
      for file in os.listdir(doomrl.path('config')):
        shutil.copy(doomrl.path('config', file), doomrl.home(file))
      with open(doomrl.home('config.lua'), 'a') as config:
        config.write('AlwaysName = "%s"\n' % doomrl.user())
      return

    if not file:
      print('Try "config <controls|colours|user>" or "help config".')
      return

    if file not in files:
      return 'Unknown file -- see "help config".'

    if reset:
      print('Restoring %s.lua to defaults.')
      shutil.copy(doomrl.path('config', '%s.lua' % file), doomrl.home())
      return

    # Use Nano in secure mode to edit the file.
    subprocess.call(
      ['nano', '-R', doomrl.home('%s.lua' % file)])

