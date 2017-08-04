import doomrl
import os
import subprocess

from commands import Command
from os.path import exists

class MortemCommand(Command):
  """mortem <player> <number> -- view a postmortem

  With no arguments, lists all players with postmortems. With a player name,
  lists the available postmortems. With a number or date, view that postmortem.

  You can also use "latest" to view the latest postmortem for that player.

  The viewer used is less(1). Use pageup/down or the arrow keys to scroll, q to
  quit. You can press h or H at any time for help.
  """

  nargs = 2

  def mortems(self, player):
    return [game for game in doomrl.games(player)
            if exists(doomrl.homepath('archive', '%d.mortem' % game['n'], user=player))]

  def list_players(self):
    """List all players with mortems, and how many."""
    print('  NUM | PLAYER')
    for player in doomrl.all_users():
      mortems = len(self.mortems(player))
      if mortems > 0:
        print(' %4d | %s' % (mortems, player))

  def run(self, player, id):
    if not player:
      return self.list_players()
    elif not doomrl.user_exists(player):
      return 'No such player: %s' % player
    elif not id:
      return doomrl.show_scores(self.mortems(player))

    mortems = self.mortems(player)
    if id == "latest":
      id = mortems[-1]['n']
    else:
      try:
        id = int(id)
      except:
        return 'Invalid mortem ID.'

    mortem = doomrl.homepath('archive', '%d.mortem' % id, user=player)
    if not exists(mortem):
      return 'No mortem with that ID found for that player.'

    try:
      subprocess.call(
        ['less', '-d', '-M', mortem],
        cwd=doomrl.homepath('archive', user=player),
        env={**os.environ, 'LESSSECURE': '1'})
    except KeyboardInterrupt:
      pass

