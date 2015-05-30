# Library for general DoomRL and DoomRL-server related manipulation

import gzip
import json
import os
import re
import subprocess
import xml.etree.ElementTree as etree

from datetime import timedelta
from os.path import join,isdir,exists

# Set up paths
_root = os.getenv('DOOMRL_SERVER') or os.path.dirname(os.path.realpath(__file__))

# Global state
_user = None
_home = None

def debug():
  return exists(path('debug')) or (_user and exists(home('debug')))

# Path manipulation
def path(*args):
  return join(_root, *args)

def home(*args, user=None):
  user = user or _user
  return join(_root, 'players', user, *args)

# User manipulation
def name_valid(name):
  """Check if a player or game name is legal."""
  return 0 < len(name) <= 24 and bytes(name, encoding='utf8').isalnum()

def login(user=None):
  """Log in (or, with no args, out)"""
  global _user,_home
  if not user:
    _user = None
    _home = None
  else:
    _user = user
    _home = home(user=user)

def user():
  return _user

def all_users():
  """A list of all doomrl-server users."""
  return sorted([
    p for p in os.listdir(path('players'))
    if isdir(home(user=p)) and not p.startswith('.')])

def user_exists(user):
  """Check if a player exists."""
  return isdir(home(user=user))


# Access to DoomRL data
def raw_mortems(user=None):
  """The contents of the user's DoomRL mortems directory."""
  return sorted(os.listdir(home('mortem', user=(user or _user))))

def raw_scores(user=None):
  """The contents of the user's score.wad."""
  difficulties = ['', 'E', 'M', 'H', 'U', 'N!']
  def fixtypes(node):
    node['difficulty'] = difficulties[int(node['difficulty'])]
    node['charname'] = node['name']
    node['name'] = user or _user
    for field in ['score', 'depth', 'level']:
      node[field] = int(node[field])
    return node

  try:
    with gzip.open(home('score.wad', user=user)) as fd:
      xml = etree.parse(fd)
    return [fixtypes(entry.attrib) for entry in xml.getroot().findall('entry')]
  except FileNotFoundError:
    return []


angels = {
  'Berserk': 'AoB',
  'Marksmanship': 'AoMr',
  'Shotgunnery': 'AoSh',
  'Light Travel': 'AoLT',
  'Impatience': 'AoI',
  'Confidence': 'AoCn',
  'Purity': 'AoP',
  'Red Alert': 'AoRA',
  'Darkness': 'AoD',
  'Max Carnage': 'AoMC',
  'Masochism': 'AoMs',
  '100': 'A100',
  'Pacifism': 'AoPc',
  'Humanity': 'AoHu',
  'Overconfidence': 'AoOC',
}

def parse_mortem(n, user=None):
  data = open(home('archive', '%d.mortem' % n, user=user), 'r').read().split('\n')
  mortem = {}

  for line in data:
    match = re.match(r" ([^,]+), level (\d+) .* (Marine|Scout|Technician),", line)
    if match:
      (mortem['name'], mortem['level'], mortem['klass']) = match.groups()
      continue
    match = re.match(r' He survived \d+ turns and scored (\d+) points\.', line)
    if match:
      mortem['score'] = int(match.group(1))
      continue
    match = re.match(r' He played for (?:(\d+) day)?.*?(?:(\d+) hour)?.*?(?:(\d+) minute)?.*?(?:(\d+) seconds?)?\.', line)
    if match:
      (d,h,m,s) = match.groups()
      mortem['time'] = ((int(d or 0) * 24 + int(h or 0)) * 60 + int(m or 0)) * 60 + int(s or 0)
      continue
    match = re.match(r' He was an Angel of (.*)!', line)
    if match:
      mortem['challenge'] = angels[match.group(1)]
      continue
    match = re.match(r' was .* by (a|an|the) (.*) (on level|at the)', line)
    if match:
      mortem['killed'] = match.group(2)
      continue
  return mortem

def games(user=None):
  """All of a player's completed games that we know of."""
  user = user or _user
  with open(home('archive', 'scores', user=user)) as fd:
    return [json.loads(line) for line in fd]

def scoreline(game, time):
  winner = (
    game['killed'] == 'nuked the Mastermind'
    or game['killed'] == 'defeated the Mastermind'
    or game['killed'] == 'completed 100 levels'
    or game['killed'] == 'completed 666 levels')
  seconds = game.get(time, 0)
  return '%s%4d | %02d:%02d:%02d %-2s%7d %-14s %sL:%-2d %-33s DL%-2d %s%s' % (
    winner and '\x1B[1m' or '',
    game['n'],
    seconds // 60 // 60,
    seconds // 60 % 60,
    seconds % 60,
    game['difficulty'],
    game['score'],
    game['name'],
    game['klass'][0].upper(),
    game['level'],
    game['killed'],
    game['depth'],
    game.get('challenge', ''),
    winner and '\x1B[0m' or '')

def show_scores(scores, time='time'):
  less = subprocess.Popen(
    ['less', '-R', '-S'],
    universal_newlines=True,
    env={'LESSSECURE': '1', 'TERM': os.getenv('TERM')},
    stdin=subprocess.PIPE)
  for score in scores:
    less.stdin.write(scoreline(score, time) + '\n')
  less.stdin.close()
  less.wait()
