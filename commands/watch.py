import doomrl
import os

from commands import Command
from datetime import timedelta
from os.path import exists
from ttyrec import resetTTY,TTYRec

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
        if exists(doomrl.homepath('ttyrec', user=player)):
          with TTYRec(path=doomrl.homepath('ttyrec', user=player)) as ttyrec:
            print("%7s %s" % (str(timedelta(seconds=int(ttyrec.ttytime()[0]))), player))
      return

    if not exists(doomrl.homepath('ttyrec', user=player)):
      return 'No game in progress under that name.'

    with TTYRec(doomrl.homepath('ttyrec', user=player)) as ttyrec:
      ttyrec.ttyplay(follow=True)
