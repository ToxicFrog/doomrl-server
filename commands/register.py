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

  def install(self, password):
    """Install a personal copy of DoomRL to the given path."""

    # Symlink in the DoomRL binary and WADs.
    for file in ['core.wad', 'doomrl', 'doomrl.wad']:
      os.symlink(doomrl.doompath(file), doomrl.homepath(file))

    # Copy in the user-editable config files, then symlink in all the rest.
    for file in ['colours.lua', 'controls.lua', 'user.lua']:
      shutil.copy(doomrl.datapath('config', file), doomrl.homepath(file))
    for file in os.listdir(doomrl.datapath('config')):
      if not exists(doomrl.homepath(file)):
        os.symlink(doomrl.datapath('config', file), doomrl.homepath(file))

    # Create directories for save files, postmortems, etc.
    for dir in ['backup', 'mortem', 'screenshot', 'saves', 'archive']:
      os.mkdir(doomrl.homepath(dir))

    # Write the password file.
    # No hashing or anything. This whole thing is fundamentally insecure, adding
    # a hash would just make it less obviously insecure without actually fixing
    # anything.
    with open(doomrl.homepath('passwd'), 'w') as passwd:
      passwd.write(password)


  def run(self, name, password):
    # Check name validity
    if not doomrl.name_valid(name):
      return 'Invalid name.'

    # Check that password was specified
    if not password:
      return 'No password specified.'

    # Try to create user directory and die if we can't
    try:
      os.mkdir(doomrl.homepath(user=name))
    except OSError as e:
      return 'That name is unavailable.'

    # Fill in user directory
    log('Creating a new account: %s' % name)
    print('Creating user account.')
    try:
      doomrl.login(name)
      self.install(password)
    except Exception as e:
      doomrl.login()
      log('Error creating account %s: %s' % (name, e))
      print('Error creating user directory.')
      print('Report this to the server administrator.')
      if doomrl.debug():
        raise e
      try:
        shutil.rmtree(doomrl.homepath(user=name))
      except OSError as e:
        log('Error cleaning up account %s: %s' % (name, e))
        print('Error cleaning up the half-created user directory! This username is unavailable until the admin fixes things.')
      return 'Unable to create user.'

    return
