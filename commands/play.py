import doomrl
import json
import os
import shutil
import subprocess
import sys
import tty

from commands import Command
from os.path import exists
from syslog import syslog as log
from ttyrec import TTYRec


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
  child = None

  def setup(self, name):
    # If the player has a game in progress, restore their ttyrec and save.
    if exists(doomrl.homepath('saves', name + '.ttyrec')):
      os.rename(doomrl.homepath('saves', name + '.ttyrec'), self.recfile)
      print('Recording of current game restored.')
    if exists(doomrl.homepath('saves', name)):
      os.rename(doomrl.homepath('saves', name), doomrl.homepath('save'))

    # Get their pre-game high scores so we can check for new ones afterwards.
    scores_before = doomrl.raw_scores()
    try:
      mortem_before = doomrl.raw_mortems()[-1]
    except IndexError:
      mortem_before = None

    return (scores_before,mortem_before)

  def run_doomrl(self):
    if exists(doomrl.datapath('ttysound', 'libSDL_mixer-1.2.so.0')):
      cmd = ['./doomrl']
      env = {
        **os.environ,
        "LD_LIBRARY_PATH": doomrl.datapath('ttysound'),
        "SDL_AUDIODRIVER": 'disk',
        'SDL_DISKAUDIOFILE': '/dev/null',
      }
    else:
      cmd = ['./doomrl', '-nosound']
      env = os.environ

    (rpipe,wpipe) = os.pipe()
    self.child = subprocess.Popen(cmd, stdout=wpipe, env=env, cwd=doomrl.homepath())
    os.close(wpipe)

    # DoomRL needs the terminal in raw mode, but since it's running inside ttyrec
    # it can't control that setting.
    tty.setraw(1)

    with TTYRec(self.recfile) as rec:
      # This will return when DoomRL closes the fd.
      # It will also automatically reset the TTY on leaving the 'with' block.
      rec.ttyrec(in_fd=rpipe)
    self.child.wait()
    self.child = None

  def run(self, name):
    if not doomrl.user():
      return 'You must log in first.'

    if not name:
      # List games in progress
      saves = os.listdir(doomrl.homepath('saves'))
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
    self.recfile = doomrl.homepath('ttyrec')
    if exists(self.recfile):
      return 'You are already playing in another window! Quit that game first.'

    (scores,mortem) = self.setup(name)
    try:
      self.run_doomrl()

    except OSError as e:
      # This almost certainly means that the user disconnected in mid-game.
      # Don't try to output any error messages, they'll just throw again because
      # our tty is gone.
      if self.child and (self.child.poll() is None):
        self.child.kill()
        self.child = None
      # Call _exit rather than using sys.exit so we don't try to run finalizers.
      os._exit(1)

    except Exception as e:
      import traceback
      log('Error running DoomRL: ' + traceback.format_exc())
      traceback.print_exc()
      sys.exit(1)
    finally:
      self.shutdown(name, scores, mortem)

  def shutdown(self, name, scores_before, mortem_before):
    # If DoomRL is still running, kill it.
    if self.child and (self.child.poll() is None):
      self.child.kill()
      self.child = None

    # If the game is still in progress, save the ttyrec file.
    if exists(doomrl.homepath('save')):
      os.rename(self.recfile, doomrl.homepath('saves', name + '.ttyrec'))
      os.rename(doomrl.homepath('save'), doomrl.homepath('saves', name))
      return

    # Otherwise, there *should* be a new high score entry and a new mortem.
    # Unless they simply didn't start a game in the first place.
    try:
      mortem = doomrl.raw_mortems()[-1]
    except IndexError:
      mortem = None

    if mortem == mortem_before:
      # No new postmortem created and no save file means no game played.
      try:
        os.remove(self.recfile)
      except FileNotFoundError:
        pass
      return

    scores_after = doomrl.raw_scores()
    n = len(scores_after)

    # Save the ttyrec and mortem files to the player archive directory.
    os.rename(self.recfile,
              doomrl.homepath('archive', '%d.ttyrec' % n))
    shutil.copy(doomrl.homepath('mortem', mortem),
                doomrl.homepath('archive', '%d.mortem' % n))

    doomrl.build_website('www')
