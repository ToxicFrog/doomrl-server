import datetime
import os
import re

from datetime import timedelta
from os.path import exists
from struct import pack,unpack
from time import time

class TTYRec(object):
  """A custom TTYRec recorder for DoomRL.

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
  def __init__(self, pipe, path, stdout=1):
    self.last_sgr = None
    self.last_pos = None
    self.last_s = int(time())
    self.delta = 0
    self.doomrl = pipe
    self.stdout = stdout

    # If the file exists, read it to determine our current timestamp
    if exists(path):
      self.set_time_from(path)

    # Open the file for append
    self.fd = open(path, "ab")

    import tty
    tty.setraw(stdout)
    tty.setcbreak(stdout)

  def __enter__(self):
    return self

  def __exit__(self, type, value, stack):
    self.fd.close()

  def set_time_from(self, path):
    with open(path, "rb") as fd:
      while True:
        header = fd.read(12)
        if not header:
          break
        (s, us, sz) = unpack("III", header)
        fd.read(sz)
        self.last_s = s

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

  def write(self, s, us, sz, data):
    # strip out garbage commands
    trimmed = re.sub(b'\x1B\\[\\d+;\\d+H', self.strip_pos, data)
    trimmed = re.sub(b'\x1B\\[[\\d;]+m', self.strip_sgr, trimmed)
    trimmed = re.sub(b'\x1B\\[\\?7l', b'', trimmed)
    if trimmed:
      # If the frame survived, write it out.
      os.write(self.stdout, data)
      #os.fsync(self.stdout)
      # Correct the timestamp first, if needed.
      if (s - self.delta) - self.last_s > 2:
        self.delta = s - self.last_s - 1
      s -= self.delta
      self.last_s = s
      self.fd.write(pack("III", s, us, sz) + data)
      self.fd.flush()

  def wait(self):
    # Now we read from the pipe and process the output until it's closed,
    # stripping out garbage frames and writing the rest to disk.
    while True:
      data = os.read(self.doomrl, 8192)
      # Split timestamp into seconds and microseconds
      ts = time()
      s = int(ts)
      us = int(ts % 1 * 1e6)
      if not data:
        break
      self.write(s, us, len(data), data)
