from commands import Command
import doomrl
import os

class DeleteCommand(Command):
  """delete <game> -- delete a game in progress.

  Delete the save file and recording associated with an in-progress game. Unlike
  loading the game and then committing suicide, this doesn't result in a high
  score entry -- the game is just gone.
  """

  nargs = 1

  def run(self, name):
    if not doomrl.user():
      return 'You must log in first.'

    saves = os.listdir(doomrl.home('saves'))
    if not name:
      # List games in progress
      if not saves:
        print('You have no games in progress.')
      else:
        print('Games in progress:')
        for save in [s for s in saves if not s.endswith('.ttyrec')]:
          print('\t', save)
        print('Type "delete <name>" to delete one.')
      return

    if not name in saves:
      return 'No such game.'

    os.remove(doomrl.home('saves', name))
    os.remove(doomrl.home('saves', name + '.ttyrec'))
    print('In-progress game ' + name + ' deleted.')

