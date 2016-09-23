import doomrl
import os
import subprocess

from commands import Command
from datetime import timedelta
from os.path import exists
from ttyrec import TTYRec

def resetTerm():
  os.write(1, '\x1Bc\x1B[!p'.encode('ascii'))

class WatchCommand(Command):
  """watch <player> -- watch an in-progress game of DoomRL.

  With no arguments, lists all currently active games. With the name of a
  player, spectates that player's game.

  The replay has an initial 'catch-up' phase where it replays the game so far
  at 64x normal speed. During this period the normal replay controls (see
  "help replay") will work. At any point you can exit spectator mode with ctrl-C.

  If the person you are spectating exits, the screen will go black and won't
  automatically return to the prompt -- this is a limitation of the underlying
  software used for replays. Once this happens, press ctrl-C to exit.
  """

  nargs = 1

  def run(self, player):
    if not player:
      # list active games
      print('   TIME PLAYER')
      for player in doomrl.all_users():
        if exists(doomrl.home('ttyrec', user=player)):
          time = int(TTYRec(path=doomrl.home('ttyrec', user=player)).ttytime()[0])
          print("%7s %s" % (str(timedelta(seconds=int(time))), player))
      return

    if not exists(doomrl.home('ttyrec', user=player)):
      return 'No game in progress under that name.'

    try:
      # First we 'catch up' by playing the replay so far at max speed.
      subprocess.call(
        ['ttyplay', '-n', 'ttyrec'],
        cwd=doomrl.home(user=player))
      # Then we peek at what remains.
      subprocess.call(
        ['ttyplay', '-p', 'ttyrec'],
        cwd=doomrl.home(user=player))
    except KeyboardInterrupt:
      pass
    finally:
      # ttyplay may leave the terminal messed up. This fixes it.
      resetTerm()

