-- Generate the closed caption files based on the contents of soundhq.lua
-- from the DRL installation.
-- We're passed the path to soundhq.lua as our first argument.
dofile((...)) -- Puts the configuration in global `Sound`

-- Utility functions for setting colours.
C = {}
for i,colour in ipairs { 'bk', 'rd', 'gr', 'yl', 'bl', 'mg', 'cy', 'wh' } do
  C[colour] = function(x) return '\x1B[0;'..(i+29)..'m'..x end
  C[colour:upper()] = function(x) return '\x1B[1;'..(i+29)..'m'..x end
end
C.O = function(x) return '\x1B[0m'..x end
C.none = function(x) return x end

local beings = require 'beings'
local events = {
  hit = { face = '*'; colour = C.RD; };
  fire = { face = '!'; colour = C.YL; };
  die = { face = '%'; colour = C.RD; };
  act = { face = ''; colour = C.none; };
  melee = { face = '!'; colour = C.yl; };
  hoof = { face = ''; colour = C.none; };
  phase = { face = '+'; colour = C.CY; };
  explode = { face = '='; colour = C.YL; };
  default = { face = ''; colour = C.none; };
}

local function symbolic(ent, evt, colour)
  evt = events[evt] or events.default
  local buf
  if not ent then
    if colour then
      buf = evt.colour(evt.face)
    else
      buf = evt.face
    end
  else
    ent = beings[ent]
    if not ent then return '' end
    if colour then
      buf = evt.colour(evt.face)
         .. ent.colour(ent.face)
         .. evt.colour(evt.face)
    else
      buf = evt.face .. ent.face .. evt.face
    end
  end
  return buf
end

local function write(file, fmt, ...)
  local fd = io.open('cc/'..file, 'w')
  fd:write(fmt:format(...))
  fd:close()
end
local function append(file, fmt, ...)
  local fd = io.open('cc/'..file, 'a')
  fd:write(fmt:format(...))
  fd:close()
end

function write_cc(style, ent, evt, fmt, ...)
  local path = style..'/'..(ent and ent..'/' or '')..evt
  write(path, fmt, ...)
  append(style..'/init.lua', 'Sound.%s%s = "cc/%s"\n',
    (ent and ent..'.' or ''),
    evt, path)
end

function write_all_cc(ent, evt, sfx)
  write_cc('sfx', ent, evt, '\x1B]666;1;%s\x07', sfx)
  write_cc('fancy', ent, evt, '%s', symbolic(ent, evt, true))
  write_cc('plain', ent, evt, '%s', symbolic(ent, evt, false))
  write_cc('fancy+sfx', ent, evt, '\x1B]666;1;%s\x07\x00%s', sfx, symbolic(ent, evt, true))
  write_cc('raw', ent, evt, '%s', evt)
end

-- For each sound effect, we want to do the following:
-- write the sound effect path (entity or entity/event) to raw/...
-- write the OSC to sfx/...
-- write the OSC and symbol to fancy+sfx/...
-- write the symbol to fancy/...
-- write the symbol without colour to plain/...
-- TODO: nightmare support
for _,style in ipairs { 'sfx', 'fancy', 'plain', 'fancy+sfx', 'raw' } do
  os.execute('mkdir -p cc/'..style)
  write(style..'/init.lua', 'Sound = {}\n')
  write_cc(style, nil, 'hoof', '')
end

for entity,events in pairs(Sound) do
  if type(events) == 'string' then
    local event = entity
    sfx = events:match('wavhq/(.*)%.wav')
    io.write(string.format("\r\x1B[2K%-16s %s", event, symbolic(nil, event, true)..C.O''))
    write_all_cc(nil, event, sfx)
  else
    io.write(string.format("\r\x1B[2K%-16s", entity))
    for _,style in ipairs { 'sfx', 'fancy', 'plain', 'fancy+sfx', 'raw' } do
      os.execute('mkdir -p cc/'..style..'/'..entity)
      append(style..'/init.lua', 'Sound.%s = {}\n', entity)
    end
    for event,sfx in pairs(events) do
      io.write(' '..symbolic(entity, event, true)..C.O'')
      sfx = sfx:match('wavhq/(.*)%.wav')
      write_all_cc(entity, event, sfx)
    end
  end
end

for entity,info in pairs(beings) do
  if not Sound[entity] and info.fallback then
    -- We have it in the beings table, but not in soundhq
    -- This probably means a boss or nightmare enemy without sound info
    io.write(string.format("\r\x1B[2K%-16s", entity))
    for _,style in ipairs { 'sfx', 'fancy', 'plain', 'fancy+sfx', 'raw' } do
      os.execute('mkdir -p cc/'..style..'/'..entity)
      append(style..'/init.lua', 'Sound.%s = {}\n', entity)
    end
    for event,sfx in pairs(Sound[info.fallback]) do
      io.write(' '..symbolic(entity, event, true)..C.O'')
      sfx = sfx:match('wavhq/(.*)%.wav')
      write_all_cc(entity, event, sfx)
    end
  end
end

print("\r\x1B[2KClosed caption data files generated.")
