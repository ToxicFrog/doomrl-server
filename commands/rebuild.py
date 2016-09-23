import doomrl
import json

from commands import Command
from os.path import exists
from ttyrec import TTYRec

class RebuildCommand(Command):
  """rebuild -- regenerate the score and mortem index. Admins only.

  This command rescans the archived postmortems and ttyrecs of each player to
  correct errors in the master score index. These errors are usually the result
  of bugs in an earlier version of doomrl-server.

  At the moment it only corrects errors in the 'time' and 'ttytime' fields.
  """

  def run(self):
    if not doomrl.debug():
      print('Server administrators only!')
      return

    for player in doomrl.all_users():
      games = doomrl.games(player)  # scores from the player's score index
      for (i,game) in enumerate(games):
        if game.get('time', 0) == 0:
          mortem = doomrl.parse_mortem(game['n'], player)
          game['time'] = mortem['time']
        if game.get('ttytime', None) is None:
          if exists(doomrl.home('archive', '%d.ttyrec' % game['n'], user=player)):
            game['ttytime'] = int(TTYRec(
              path=doomrl.home('archive/%d.ttyrec' % game['n'],
                               user=player)
              ).ttytime()[0])
          else:
            game['ttytime'] = 0  # no replay available
      with open(doomrl.home('archive', 'scores', user=player), "w") as fd:
        for game in games:
          fd.write(json.dumps(game) + '\n')
      print('%s: rebuilt %d records' % (player, len(games)))

    doomrl.build_website('www')


