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

  def reset(self, file):
    print('Restoring %s to defaults.' % file)
    shutil.copy(doomrl.datapath('config', "%s.lua" % file), doomrl.homepath("%.lua" % file))


  def run(self, file, reset):
    if not doomrl.user():
      return 'You must be logged in.'

    if reset and reset != 'reset':
      return 'Invalid second argument. See "help config".'

    files = frozenset(['controls', 'colours', 'user'])

    if reset and file == "all":
      for file in files:
        reset(file)
      return

    if not file or file not in files:
      print('Try "config <controls|colours|user>" or "help config".')
      return

    if reset:
      reset(file)
      return

    # Use Nano in secure mode to edit the file.
    subprocess.call(
      ['nano', '-R', doomrl.homepath('%s.lua' % file)])

