import doomrl
import os
import shutil

from commands import Command, run_command
from os.path import join, exists
from syslog import syslog as log

class RegisterCommand(Command):
  """register <name> <pass> -- create a new account

  Attempts to create (and log in to) a new user account. You can spectate and
  view the high score list as a guest, but in order to actually play you need to
  register.

  The username will be used as both your login username and your DoomRL username
  (and thus will appear on the high score list) and has certain restrictions as
  a result: 24 character maximum, alphanumeric ASCII only. The password can
  contain anything, including whitespace."""

  nargs = 2

  def install(self, home, name, password):
    """Install a personal copy of DoomRL to the given path."""
    # The player gets symlinks to the doomrl binary and wad files. They get
    # their own personal backup, mortem, screenshot, and recording directories,
    # and their own personal config files (so that they can be edited).
    for file in ['core.wad', 'doomrl', 'doomrl.wad']:
      os.symlink(join('../../doomrl', file), doomrl.home(file, user=name))
    for file in ['colours.lua', 'controls.lua', 'user.lua']:
      shutil.copy(doomrl.path('config', file), doomrl.home(file, user=name))
    for file in os.listdir(doomrl.path('config')):
      if not exists(doomrl.home(file, user=name)):
        os.symlink(join('../../config', file), doomrl.home(file, user=name))
    for dir in ['backup', 'mortem', 'screenshot', 'saves', 'archive']:
      os.mkdir(join(home, dir))
    with open(join(home, 'passwd'), 'w') as passwd:
      passwd.write(password)
    # Create empty scores file
    open(join(home, 'archive', 'scores'), 'w').close()


  def run(self, name, password):
    # Check name validity
    if not doomrl.name_valid(name):
      return 'Invalid name.'

    # Check that password was specified
    if not password:
      return 'No password specified.'

    # Try to create user directory and die if we can't
    home = doomrl.home(user=name)
    try:
      os.mkdir(home)
    except OSError as e:
      return 'That name is unavailable.'

    # Fill in user directory
    log('Creating a new account: %s' % name)
    print('Creating user account.')
    try:
      self.install(home, name, password)
    except Exception as e:
      log('Error creating account %s: %s' % (name, e))
      print('Error creating user directory.')
      print('Report this to the server administrator.')
      if doomrl.debug():
        raise e
      try:
        shutil.rmtree(home)
      except OSError as e:
        log('Error cleaning up account %s: %s' % (name, e))
        print('Error cleaning up the half-created user directory! This username is unavailable until the admin fixes things.')
      finally:
        doomrl.login()
        return 'Unable to create user.'

    # Login
    return run_command('login', '%s %s' % (name, password))
