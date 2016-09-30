import doomrl
import json
import os
import shutil
import subprocess
import sys
import tty

from commands import Command
from os.path import exists
from ttyrec import TTYRec

def resetTerm():
  os.write(1, '\x1Bc\x1B[!p'.encode('ascii'))

class PlayCommand(Command):
  """play <name> -- start or continue a game of DoomRL.

  Without arguments, list your saved games. With a name, start or resume a game
  with that name.

  The game will automatically be recorded and made available for spectating.

  If you save and quit, the savegame will be automatically archived under the
  name you chose. You can resume it later by providing the same name, or start
  a new game in parallel by providing a different one. This allows you to (for
  example) have a long running Angel of 666 game in one save, while still taking
  breaks for shorter standard games.
  """

  nargs = 1

  def setup(self, name):
    # If the player has a game in progress, restore their ttyrec and save.
    if exists(doomrl.home('saves', name + '.ttyrec')):
      os.rename(doomrl.home('saves', name + '.ttyrec'), self.recfile)
      print('Recording of current game restored.')
    if exists(doomrl.home('saves', name)):
      os.rename(doomrl.home('saves', name), doomrl.home('save'))

    # Get their pre-game high scores so we can check for new ones afterwards.
    scores_before = doomrl.raw_scores()
    try:
      mortem_before = doomrl.raw_mortems()[-1]
    except IndexError:
      mortem_before = None

    return (scores_before,mortem_before)

  def run_doomrl(self):
    if exists(doomrl.path('ttysound', 'libSDL_mixer-1.2.so.0')):
      cmd = ['./doomrl']
      env = {
        "LD_LIBRARY_PATH": doomrl.path('ttysound'),
        "SDL_AUDIODRIVER": 'disk',
        'SDL_DISKAUDIOFILE': '/dev/null',
        'TERM': os.getenv('TERM'),
      }
    else:
      cmd = ['./doomrl', '-nosound']
      env = { 'TERM': os.getenv('TERM') }

    (rpipe,wpipe) = os.pipe()
    child = subprocess.Popen(cmd, stdout=wpipe, env=env, cwd=doomrl.home())
    os.close(wpipe)

    # DoomRL needs the terminal in raw mode, but since it's running inside ttyrec
    # it can't control that setting.
    tty.setraw(1)

    with TTYRec(self.recfile) as rec:
      # This will return when DoomRL closes the fd.
      rec.ttyrec(in_fd=rpipe)
    child.wait()

  def run(self, name):
    if not doomrl.user():
      return 'You must log in first.'

    if not name:
      # List games in progress
      saves = os.listdir(doomrl.home('saves'))
      if not saves:
        print('You have no games in progress.')
      else:
        print('Games in progress:')
        for save in [s for s in saves if not s.endswith('.ttyrec')]:
          print('\t', save)
        print('Type "play <name>" to resume one.')
      return

    # We can be a bit looser about names here, but for simplicity's sake we
    # just reuse the name validation code we use for player names.
    if not doomrl.name_valid(name):
      return 'Invalid save name.'

    # Check that they aren't already playing *right now*.
    self.recfile = doomrl.home('ttyrec')
    if exists(self.recfile):
      return 'You are already playing in another window! Quit that game first.'

    (scores,mortem) = self.setup(name)
    try:
      self.run_doomrl()
    except Exception as e:
      import traceback
      log('Error running DoomRL: ' + traceback.format_exc())
      # If something went wrong while playing DoomRL, the terminal is probably
      # completely hosed and there may still be processes running in the
      # background. Nothing to do here but die and hope the SIGHUP gets them.
      resetTerm()
      traceback.print_exc()
      sys.exit(1)
    finally:
      resetTerm()
      self.shutdown(name, scores, mortem)

  def shutdown(self, name, scores_before, mortem_before):
    # If the game is still in progress, save the ttyrec file.
    if exists(doomrl.home('save')):
      os.rename(self.recfile, doomrl.home('saves', name + '.ttyrec'))
      os.rename(doomrl.home('save'), doomrl.home('saves', name))
      return

    # Otherwise, there *should* be a new high score entry and a new mortem.
    # Unless they simply didn't start a game in the first place.
    try:
      mortem = doomrl.raw_mortems()[-1]
    except IndexError:
      mortem = None

    if mortem == mortem_before:
      # No new postmortem created and no save file means no game played.
      os.remove(self.recfile)
      return

    scores_after = doomrl.raw_scores()
    n = len(scores_after)

    # Save the ttyrec and mortem files to the player archive directory.
    os.rename(self.recfile,
              doomrl.home('archive', '%d.ttyrec' % n))
    shutil.copy(doomrl.home('mortem', mortem),
                doomrl.home('archive', '%d.mortem' % n))

    doomrl.build_website('www')
