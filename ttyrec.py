import datetime
import os
import re
import termios
import tty

from datetime import timedelta
from os.path import exists
from select import select
from struct import pack,unpack
from time import time, sleep

def resetTTY(stdin=0, stdout=1):
  # Reset the TTY by sending hard and soft terminal reset strings.
  os.write(stdout, b'\x1Bc\x1B[!p')
  # Reset the TTY controller using termios. This should be roughly equivalent to 'stty cooked'.
  attr = termios.tcgetattr(stdin)
  attr[0] |= termios.BRKINT | termios.IGNPAR | termios.ISTRIP | termios.ICRNL | termios.IXON
  attr[1] |= termios.ONLCR | termios.OPOST
  attr[3] |= termios.ECHO | termios.ECHONL | termios.ICANON | termios.ISIG | termios.IEXTEN
  termios.tcsetattr(stdin, termios.TCSADRAIN, attr)


class TTYRec(object):
  """A custom TTYRec implementation for DoomRL.

  This class needs a bit of explanation. See, DoomRL's tty handling code is kind
  of buggy and constantly spams no-op commands even when nothing is happening.
  This has two unfortunate consequences: the ttyrec files are huge, and ttyplay
  can't skip large sections of inactivity (because everything looks like
  activity all the time).

  This class does two things. First, it automatically drops frames which
  consist only of these no-op commands (in a kind of hackish way, but it works).
  Second, it adjusts the frame timing to trim out large periods of inactivity
  (which may range from seconds to -- if a game was resumed from save after a
  long period of inactivity -- weeks or more).

  It completely replaces the use of ttyrec; this class simultaneously filters
  the output of DoomRL and writes the ttyrec file.
  """
  def __init__(self, path, reset=False):
    self.path = path
    self.reset_tty = reset

  def __enter__(self):
    if exists(self.path):
      self.fd = open(self.path, 'r+b')
    else:
      self.fd = open(self.path, 'w+b')
    return self

  def __exit__(self, type, value, stack):
    if self.reset_tty:
      resetTTY()
    self.fd.close()

  def next_frame(self):
    header = self.fd.read(12)
    if not header:
      return None
    (s, us, sz) = unpack("III", header)
    data = self.fd.read(sz)
    return (s + float(us)/1e6, data)

  def frames(self):
    frame = self.next_frame()
    while frame is not None:
      yield frame
      frame = self.next_frame()

  def rewind(self):
    self.fd.seek(0)

  ### ttytime(1) ###

  def ttytime(self):
    """Similar to ttytime(1). Returns a (length, start, end) tuple; length is the
    total length of the recording, start and end the absolute timestamps of the
    first and last frames.
    """
    self.rewind()
    frame = self.next_frame()
    if frame is None:
      return 0, time(), time()
    start_ts = frame[0]
    for ts,_ in self.frames():
      end_ts = ts
    return (end_ts - start_ts), start_ts, end_ts


  ### ttyrec(1) ###

  def strip_pos(self, match):
    if match.group(0) == self.last_pos:
      return b''
    self.last_pos = match.group(0)
    return match.group(0)

  def strip_sgr(self, match):
    if match.group(0) == self.last_sgr:
      return b''
    self.last_sgr = match.group(0)
    return match.group(0)

  def write_frame(self, ts, data):
    # Remove redundant SGR and cursor positioning commands.
    trimmed = re.sub(b'\x1B\\[\\d+;\\d+H', self.strip_pos, data)
    trimmed = re.sub(b'\x1B\\[[\\d;]+m', self.strip_sgr, trimmed)
    # Remove redundant DECRST[wraparound mode] commands.
    trimmed = re.sub(b'\x1B\\[\\?7l', b'', trimmed)
    if trimmed:
      # If there's anything left of the frame after stripping no-ops, write it
      # to the recording.
      # Correct the timestamp first, if needed.
      if (ts - self.delta) - self.last_ts > 2:
        self.delta = ts - self.last_ts - 1
      ts -= self.delta
      self.last_ts = ts
      self.fd.write(pack("III", int(ts), int(ts%1 * 1e6), len(data)) + data)
      self.fd.flush()
      return data

  def ttyrec(self, in_fd, out_fd=1):
    """Create or append to a recording with the contents of in_fd.

    If out_fd is specified, additionally writes the stripped data to it. This
    is usually stdout.

    If the terminal needs to be in raw mode (hint: it almost certainly does),
    it's up to the caller to arrange this.
    """

    # Set up the initial state for recording.
    self.reset_tty = True
    self.last_sgr = None
    self.last_pos = None
    self.delta = 0
    self.last_ts = self.ttytime()[2] # this also seeks to the end of the file

    # Now we read from the pipe and process the output until it's closed,
    # stripping out garbage frames and writing the rest to disk.
    while True:
      data = os.read(in_fd, 8192)
      if not data:
        break
      data = self.write_frame(time(), data)
      if data and out_fd:
        os.write(out_fd, data)

  ### ttyplay(1) ###
  # This is complicated enough that it has its own class (TTYPlayer).

  def ttyplay(self, follow=False, **kwargs):
    self.reset_tty = True
    player = TTYPlayer(self, **kwargs)
    if follow:
      player.follow()
    else:
      player.play()


_keybinds = {}
def keybind(*keys):
  def wrap(fn):
    for k in keys:
      _keybinds[bytes(k, 'ascii')] = fn
    return fn
  return wrap

class TTYPlayer(object):
  """An interactive player for ttyrec files. This is complicated enough and has
  enough state that it gets its own class.

  It should not be instantiated directly; instead, create and play a TTYRec:
  with TTYRec(path) as ttyrec:
    ttyrec.ttyplay(...arguments to TTYPlayer constructor...)
  """

  class QuitException(Exception):
    pass
  class InvalidateFrameException(Exception):
    pass

  speed = 1.0

  def __init__(self, ttyrec, stdin=0, stdout=1, osd_line=1, osd_width=80):
    self.ttyrec = ttyrec
    self.osd_line = osd_line
    self.osd_width = osd_width
    self.stdin = stdin
    self.stdout = stdout

    ttyrec.rewind()
    (self.duration, self.start, self.end) = ttyrec.ttytime()
    self.position = 0.0
    ttyrec.rewind()

  ### Keybinds ###

  @keybind('f', '=', '+')
  def faster(self):
    self.speed *= 2.0

  @keybind('s', '-', '_')
  def slower(self):
    self.speed /= 2.0

  @keybind('1')
  def realtime(self):
    self.speed = 1.0

  @keybind(',')
  def seek_back(self):
    self.seek_to(max(self.position-60, 0.0))

  @keybind('.')
  def seek_forward(self):
    self.seek_to(min(self.position+60, self.duration))

  @keybind('<')
  def seek_back_long(self):
    self.seek_to(max(self.position-600, 0.0))

  @keybind('>')
  def seek_forward_long(self):
    self.seek_to(min(self.position+600, self.duration))

  @keybind('[')
  def seek_back_short(self):
    self.seek_to(max(self.position-6, 0.0))

  @keybind(']')
  def seek_forward_short(self):
    self.seek_to(min(self.position+6, self.duration))

  pause = False
  @keybind(' ')
  def pause(self):
    self.pause = not self.pause

  def dispatch_command(self, key):
    """Given a key, run the corresponding key handler, then display the status
    OSD for one second (or until another key is pressed) before resuming playback."""
    if key not in _keybinds:
      # Unknown command.
      self.osd('Unknown command: ' + key.decode('ascii'))
      select([self.stdin], [], [], 1.0)
      self.osd('')
      return
    try:
      _keybinds[key](self)
    finally:
      self.status()
      select([self.stdin], [], [], 1.0)
      self.osd('')

  def osd(self, str):
    """Display the given string on screen."""
    # Save cursor position, then move cursor to target row and erase line.
    # \x1B[1;37;44m
    os.write(1, b'\x1B[s\x1B[%d;1H\x1B[2K' % self.osd_line)
    # Display message.
    os.write(1, str.encode('utf8'))
    # Restore old cursor position.
    os.write(1, b'\x1B[u')

  def progress_bar(self, width):
    """Return a textual progress bar that looks like |--0--| scaled to fit in
    'width' columns."""
    position = (self.position/self.duration) * (width-2)
    return ('|' + '-' * int(position) + '0' + '-' * int(width-3-position) + '|')

  def status(self):
    """Display the current status -- timestamp/duration, progress bar, and speed
    -- using osd()."""
    if self.pause:
      speed = "PAUSE"
    elif self.speed >= 1:
      speed = '%dx' % self.speed
    else:
      speed = '1/%dx' % (1.0/self.speed)

    position = ' %d:%02d / %d:%02d' % (
      self.position/60, self.position % 60,
      self.duration/60, self.duration % 60)

    self.osd('%s %s %s' % (
      position,
      self.progress_bar(self.osd_width - len(speed) - len(position) - 2),
      speed))

  def seek_to(self, when):
    """Seek to the given timestamp (as seconds since the start of the file, not
    seconds since epoch). If seeking forward, just outputs the needed frames.
    If seeking backwards, rewinds to the beginning first to ensure that the tty
    is consistent.
    WARNING: seeking backwards can be extremely expensive because of this.
    TODO: keyframe support.
    """
    if when < self.position:
      self.ttyrec.rewind()
      self.position = 0.0

    for ts,data in self.ttyrec.frames():
      self.position = ts - self.start
      self.prev_ts = ts
      os.write(self.stdout, data)
      if ts - self.start >= when:
        raise self.InvalidateFrameException()

  prev_ts = 0.0
  def next_frame(self):
    """Like TTYRec.next_frame, except:

    - it returns (time to display frame, data) instead of (absolute ts of frame, data)
    - at EOF, it returns (0.25, b'') instead of None, to implement "follow mode"
    """
    frame = self.ttyrec.next_frame()
    if frame is None:
      self.position = self.duration
      return (0.25, b'')

    if frame[0] > self.end:
      self.end = frame[0]
      self.duration = self.end - self.start

    duration = frame[0] - self.prev_ts
    self.position = frame[0] - self.start
    self.prev_ts = frame[0]
    return (duration, frame[1])

  def wait_frame(self, duration):
    """Wait out the gap between one frame and the next. While waiting, process user input."""
    while duration > 0:
      now = time()
      (fdin,_,_) = select([self.stdin], [], [], duration/self.speed)
      if not self.pause:
        duration -= (time() - now) * self.speed
      if fdin:
        char = os.read(self.stdin, 1)
        if char == b'q':
          raise self.QuitException()
        else:
          self.dispatch_command(char)

  def play(self, start_at=0.0):
    """Play the contents of the file interactively."""
    tty.setraw(self.stdout)
    self.ttyrec.rewind()
    self.pause = False

    try:
      self.seek_to(start_at)
    except self.InvalidateFrameException:
      pass

    while True:
      frame = self.next_frame()
      try:
        self.wait_frame(frame[0])
      except self.QuitException:
        return
      except self.InvalidateFrameException:
        continue
      os.write(self.stdout, frame[1])

  def follow(self):
    self.play(start_at=self.duration)


if __name__ == "__main__":
  import sys
  with TTYRec(sys.argv[1]) as ttyrec:
    ttyrec.ttyplay()
