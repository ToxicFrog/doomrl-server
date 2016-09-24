import doomrl
import json

from commands import Command
from os.path import exists
from ttyrec import TTYRec

class RebuildCommand(Command):
  """rebuild -- regenerate the score and mortem index. Admins only.

  This command rescans the archived postmortems and ttyrecs of each player and
  rebuilds the cached score information and website based on what it finds.

  If you run it with any argument, it will rebuild all game information even
  if no errors are detected in the cached information.
  """
  nargs = 1

  def run(self, force):
    if not doomrl.debug():
      print('Server administrators only!')
      return

    doomrl.build_website('www')
