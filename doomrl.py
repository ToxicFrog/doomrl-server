# Library for general DoomRL and DoomRL-server related manipulation

import gzip
import json
import os
import re
import subprocess
import xml.etree.ElementTree as etree

from os.path import join,isdir,exists
from collections import defaultdict

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
  'Travel': 'AoLT',
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

matchers = {
  r' ([^,]+), level (\d+) .* (Marine|Scout|Technician),':
  lambda name, level, klass: { 'charname': name, 'level': int(level), 'klass': klass },

  # Sometimes you get a version where the charname is on a separate line! wriiiiiiii
  r' level (\d+) .* (Marine|Scout|Technician),':
  lambda level, klass: { 'level': int(level), 'klass': klass },

  # Not all of them has "was". This is definitely a bug in DoomRL, since you end
  # up with journal lines saying "on level N, he finally killed by a whatever".
  r' (?:was )?(?:.*) by ((?:a|an|the) .*) (?:on level|at the)':
  lambda killer: { 'killed': "killed by " + killer },

  r" (?:got too close to a (cacodemon)"
  r"|couldn't evade a (revenant)'s fireball"
  r"|rode a (mancubus) rocket"
  r"|let an (arachnotron) get him"
  r"|was melted by (former commando)'s plasma gun"
  r"|let the (Spider Mastermind) pwn him"
  r") .*":
  lambda *args: { 'killed': "killed by a " + [x for x in args if x][0] },

  r" committed a stupid suicide.*": lambda: { 'killed': 'committed suicide' },
  r" ((?:defeated|nuked) the Mastermind|nuked himself|completed 100 levels) .*":
  lambda win: { 'killed': win },

  r' He survived \d+ turns and scored (\d+) points\.':
  lambda score: { 'score': int(score) },

  r' He played for (?:(\d+) day)?.*?(?:(\d+) hour)?.*?(?:(\d+) minute)?.*?(?:(\d+) seconds?)?\.':
  lambda d, h, m, s: { 'time': ((int(d or 0) * 24 + int(h or 0)) * 60 + int(m or 0)) * 60 + int(s or 0) },

  # Difficulty levels.
  r" He was too young to die!":            lambda: { 'difficulty': 'E' },
  r" He didn't like it too rough.":        lambda: { 'difficulty': 'M' },
  r" He wasn't afraid to be hurt plenty.": lambda: { 'difficulty': 'H' },
  r" He was a man of Ultra-Violence!":     lambda: { 'difficulty': 'U' },
  r" He opposed the Nightmare!":           lambda: { 'difficulty': 'N!'},

  r' He was an Angel of (.*)!':
  lambda challenge: { 'challenge': angels[challenge] },

  r' He was an Archangel of (.*)!':
  lambda challenge: { 'challenge': 'A' + angels[challenge] },

  r' He was also an Angel of (.*)!':
  lambda challenge: { 'challenge2': angels[challenge] },

  # Calculate depth from the deepest level that shows up in the journal.
  r'  On level (\d+) .*': lambda dl: { 'depth': int(dl) },
  r'  He nuked level (\d+)!': lambda dl: { 'depth': int(dl) },

  # Sometimes the morten says "defeated the Mastermind" at the start even when
  # it was a full win. So, look for the journal entry about killing Carmack.
  r'  Then finally in Hell itself, he killed the final EVIL\.':
  lambda: { 'killed': 'nuked the Mastermind', 'depth': 25 },
}

def parse_mortem(n, user=None):
  data = open(home('archive', '%d.mortem' % n, user=user), 'r').read().split('\n')
  mortem = { 'n': n, 'name': user }

  for line in data:
    for regex,handler in matchers.items():
      match = re.match(regex, line)
      if match:
        mortem.update(handler(*match.groups()))
        break

  return mortem

def games(user=None):
  """All of a player's completed games that we know of."""
  user = user or _user
  return [
    parse_mortem(int(filename.replace('.mortem', '')), user=user)
    for filename in os.listdir(home('archive', user=user))
    if filename.endswith('.mortem')
  ]

def winner(game):
  return (
    game['killed'] == 'nuked the Mastermind'
    or game['killed'] == 'defeated the Mastermind'
    or game['killed'] == 'completed 100 levels'
    or game['killed'] == 'completed 666 levels')

def scoreline(game, time='time', bold='\x1B[1m', bold_eol='\x1B[0m'):
  seconds = game.get(time, 0)
  return '%s%4d | %02d:%02d:%02d %-2s%7d %-14s %sL:%-2d %-33s DL%-2d %s %s%s' % (
    winner(game) and bold or '',
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
    game.get('challenge2', ''),
    winner(game) and bold_eol or '')

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

# Website structure:
# www/index.html: top N scores and top killers
# www/players/index.html: list of players with K/D ratio for each, click for specific player
# www/players/<name>/index.html: page listing all of that player's games
# www/players/<name>/<index>.{mortem,ttyrec}: postmortem and ttyrec files
# www/players/<name>/<name>.zip: archive of all postmortem and ttyrec files
_HEADER = (
  '<html><head>'
  '<style>a:link { color: #0080FF; } a:visited { color: #8000FF };</style>'
  '<title>DoomRL</title></head>'
  '</head><body style="color: #FFFFFF; background-color: #000000;">'
  '<div style="text-align:center;">'
  '<pre style="text-align:left; display:inline-block;">')
_FOOTER = '</pre></div></body></html>'

def path_to(user, type, game):
  return home('archive', '%d.%s' % (game['n'], type), user=user)

def link_to(www, user, file):
  dst = join(www, 'players', user, file)
  src = home('archive', file, user=user)
  if exists(dst):
    return True
  if exists(src):
    os.link(src, dst)
    return True
  return False

def build_website_for_user(www, user):
  user_games = games(user)
  user_games.sort(reverse=True, key=lambda s: int(s['score']))

  if not exists(join(www, 'players', user)):
    os.makedirs(join(www, 'players', user))
  with open(join(www, 'players', user, 'index.html'), 'w') as fd:
    fd.write(_HEADER)
    if len(user_games) == 0:
      fd.write("This user hasn't played any games yet.\n")
    else:
      for game in user_games:
        if link_to(www, user, '%d.mortem' % game['n']):
          fd.write('[<a href="%d.mortem">LOG</a>]' % game['n'])
        else:
          fd.write('[   ]')
        if link_to(www, user, '%d.ttyrec' % game['n']):
          fd.write('[<a href="../../replay.html#%s/%d">TTY</a>]' % (user, game['n']))
        else:
          fd.write('[   ]')
        fd.write(scoreline(game, bold='<b>', bold_eol='</b>') + '\n')
    fd.write(_FOOTER)
  return user_games

def build_website(www):
  www = join(_root, www)
  all_games = []
  if not exists(join(www, 'players')):
    os.makedirs(join(www, 'players'))
  with open(join(www, 'players', 'index.html'), 'w') as fd:
    fd.write(_HEADER)
    fd.write('wins / total\n')
    for user in all_users():
      # create/update per-player directory
      user_games = build_website_for_user(www, user)
      if not len(user_games):
        continue
      all_games += user_games
      fd.write(' %3d / %-3d  <a href="%s/index.html">%s</a>\n' % (
        len([g for g in user_games if winner(g)]),
        len(user_games),
        user,
        user))
    fd.write(_FOOTER)

  # create/update master index
  all_games.sort(reverse=True, key=lambda s: int(s['score']))
  with open(join(www, 'index.html'), 'w') as fd:
    fd.write(_HEADER)
    if exists(path('webmotd')):
      fd.write(open(path('webmotd'), 'r').read())
    else:
      fd.write(open(path('webmotd.default'), 'r').read())
    fd.write('<hr>\n<div style="text-align:center">'
             '[<a href="players/index.html">By Player</a>]'
             '[<a href="deaths.html">Top Deaths</a>]'
             '</div>\n')
    for game in all_games:
      user = game['name']
      n = game['n']
      if exists(join(www, 'players', user, '%d.mortem' % n)):
        fd.write('[<a href="players/%s/%d.mortem">LOG</a>]' % (user, n))
      else:
        fd.write('[   ]')
      if exists(join(www, 'players', user, '%d.ttyrec' % n)):
        fd.write('[<a href="replay.html#%s/%d">TTY</a>]' % (user, n))
      else:
        fd.write('[   ]')
      fd.write(scoreline(game, bold='<b>', bold_eol='</b>') + '\n')
    fd.write(_FOOTER)

  # create/update death scoreboard
  all_deaths = defaultdict(int)
  for game in all_games:
    killed = game['killed']
    all_deaths[killed] += 1
  with open(join(www, 'deaths.html'), 'w') as fd:
    fd.write(_HEADER)
    for (death,count) in sorted(all_deaths.items(), reverse=True, key=lambda x: x[1]):
      fd.write('%4d %s\n' % (count, death))
    fd.write(_FOOTER)
