import doomrl
import os
import subprocess

from commands import Command
from os.path import exists
from ttyrec import TTYRec

class ReplayCommand(Command):
  """replay <player> <number> -- replay a recorded game

  With no arguments, lists all players with recorded games. With a player name,
  lists the recorded games for that player. With a name and a replay number,
  replays the given name. The replay number can be found out from the list of
  that player's replays.

  You can also use "latest" to view the latest replay for that player.

  Replay controls:
    f or +: go faster
    s or -: go slower
    1: reset speed
    q: exit replay
  """

  nargs = 2

  def replays(self, player):
    return [game for game in doomrl.games(player)
            if exists(doomrl.home('archive', '%d.ttyrec' % game['n'], user=player))]

  def list_players(self):
    """List all players with recordings, and how many."""
    print('  NUM | PLAYER')
    for player in doomrl.all_users():
      replays = len(self.replays(player))
      if replays > 0:
        print(' %4d | %s' % (replays, player))

  def run(self, player, id):
    if not player:
      return self.list_players()
    elif not doomrl.user_exists(player):
      return 'No such player: %s' % player
    elif not id:
      # FIXME: this currently shows the play time, not the ttyrec time.
      # This is because, with the new on-the-fly mortem parsing and elimination
      # of the score cache, determining the ttyrec time on the fly requires
      # reading all of the player's ttyrec files start to finish, which may be
      # hundreds of megabytes if they've played a lot of games, and we don't
      # want to do that every time someone types 'scores'.
      return doomrl.show_scores(self.replays(player))

    # Replay the named recording.
    replays = self.replays(player)
    if id == "latest":
      id = replays[-1]['n']
    else:
      try:
        id = int(id)
      except:
        return 'Invalid replay ID.'

    replay = doomrl.home('archive', '%d.ttyrec' % id, user=player)
    if not exists(replay):
      return 'No replay with that ID found for that player.'

    with TTYRec(replay) as ttyrec:
      ttyrec.ttyplay(osd_line=26)
