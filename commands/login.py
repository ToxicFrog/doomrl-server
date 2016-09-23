from commands import Command
import doomrl
from syslog import syslog as log

class LoginCommand(Command):
  """login <name> <pass> -- log in to an existing account.

  This is necessary in order to actually play games. To create a new account,
  use "register"."""

  nargs = 2

  def run(self, name, password):
    if doomrl.user():
      return 'You are already logged in!'

    if not name or not password:
      return 'You must specify both a username and a password.'

    # Check password
    try:
      with open(doomrl.home('passwd', user=name)) as f:
        passwd = f.read()
      if passwd == password:
        log('%s successfully logged in.' % name)
        doomrl.login(name)
        return
    except IOError as e:
      pass

    log('Failed login attempt as %s' % name)
    doomrl.login()
    return 'Login failed.'
