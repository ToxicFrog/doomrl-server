import datetime
import os
import re
import tty

from datetime import timedelta
from os.path import exists
from select import select
from struct import pack,unpack
from time import time

def next_frame(fd):
  header = fd.read(12)
  if not header:
    return None
  (s, us, sz) = unpack("III", header)
  data = fd.read(sz)
  return (s + float(us)/1e6, data)

def frames(fd):
  frame = next_frame(fd)
  while frame is not None:
    yield frame
    frame = next_frame(fd)

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
  def __init__(self, path):
    self.path = path

  def __enter__(self):
    return self

  def __exit__(self, type, value, stack):
    pass


  ### ttytime(1) ###

  def ttytime(self):
    """Similar to ttytime(1). Returns a (length, start, end) tuple; length is the
    total length of the recording, start and end the absolute timestamps of the
    first and last frames.
    """
    with open(self.path, "rb") as fd:
      start_ts = next_frame(fd)[0]
      for ts,_ in frames(fd):
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

  def write_frame(self, fd, ts, data):
    # strip out garbage commands
    trimmed = re.sub(b'\x1B\\[\\d+;\\d+H', self.strip_pos, data)
    trimmed = re.sub(b'\x1B\\[[\\d;]+m', self.strip_sgr, trimmed)
    trimmed = re.sub(b'\x1B\\[\\?7l', b'', trimmed)
    if trimmed:
      # If there's anything left of the frame after stripping no-ops, write it
      # to the recording.
      # Correct the timestamp first, if needed.
      if (ts - self.delta) - self.last_ts > 2:
        self.delta = ts - self.last_ts - 1
      ts -= self.delta
      self.last_ts = ts
      fd.write(pack("III", int(ts), int(ts%1 * 1e6), len(data)) + data)
      fd.flush()
      return data

  def ttyrec(self, in_fd, out_fd=1):
    """Create or append to a recording with the contents of in_fd.

    If out_fd is specified, additionally writes the stripped data to it. This
    is usually stdout.

    If the terminal needs to be in raw mode (hint: it almost certainly does),
    it's up to the caller to arrange this.
    """

    # Set up the initial state for recording.
    self.last_sgr = None
    self.last_pos = None
    self.delta = 0
    if exists(self.path):
      self.last_ts = self.ttytime()[2] # end time of recording
    else:
      self.last_ts = time()

    # Open the file for append
    with open(self.path, "ab") as ttyrec:
      # Now we read from the pipe and process the output until it's closed,
      # stripping out garbage frames and writing the rest to disk.
      while True:
        data = os.read(in_fd, 8192)
        if not data:
          break
        data = self.write_frame(ttyrec, time(), data)
        if data and out_fd:
          os.write(out_fd, data)


  ### ttyplay(1) ###

  def ttyplay(self, stdin=0, stdout=1):
    speed = 1.0
    tty.setraw(stdout)
    with open(self.path, "rb") as fd:
      (old_ts,data) = next_frame(fd)
      os.write(stdout, data)
      for ts,data in frames(fd):
        now = time()
        frame_time = ts - old_ts
        while frame_time > 0:
          (fdin,_,_) = select([stdin], [], [], frame_time/speed)
          if fdin:
            # process input from user
            char = os.read(stdin, 1)
            if char == b'q':
              sys.exit(0)
            elif char == b'f':
              speed *= 2.0
            elif char == b's':
              speed *= 0.5
            elif char == b'1':
              speed = 1.0
            frame_time -= time() - now
          else:
            frame_time = 0
        os.write(stdout,data)
        old_ts = ts


if __name__ == "__main__":
  import sys
  TTYRec(sys.argv[1]).ttyplay()
