# Library for general DoomRL and DoomRL-server related manipulation

import gzip
import json
import os
import xml.etree.ElementTree as etree

from os.path import join,isdir,exists

# Set up paths
_root = os.getenv('DOOMRL_SERVER') or os.path.dirname(os.path.realpath(__file__))

# Global state
_user = None
_home = None

def debug():
  return True or _user and exists(home('debug'))

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

def games(user=None):
  """All of a player's completed games that we know of."""
  user = user or _user
  with open(home('archive', 'scores', user=user)) as fd:
    return [json.loads(line) for line in fd]

def scoreline(game):
  return ' %4d | %2s %7d %-24s %sL:%-2d %-34s DL%-2d %s' % (
    game['n'],
    game['difficulty'],
    game['score'],
    game['name'],
    game['klass'][0].upper(),
    game['level'],
    game['killed'],
    game['depth'],
    game.get('challenge', ''))
