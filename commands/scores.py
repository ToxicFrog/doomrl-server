import doomrl

from commands import Command

class ScoresCommand(Command):
  """scores [player] -- show high score list

  With no arguments, show the entire scoreboard. With a given player, show only
  scores for that player. Use the arrow keys or pageup/down to scroll, and q to
  quit.

  Note that due to restrictions on how DoomRL stores the high score list, the
  in-game high scores will always only show your own."""

  nargs = 1

  def run(self, player):
    if not player:
      games = []
      for player in doomrl.all_users():
        games += doomrl.games(player)
    else:
      games = doomrl.games(player)

    games.sort(reverse=True, key=lambda s: int(s['score']))
    doomrl.show_scores(games)

