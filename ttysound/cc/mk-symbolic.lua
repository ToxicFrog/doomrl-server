C = {} -- global
for i,colour in ipairs { 'bk', 'rd', 'gr', 'yl', 'bl', 'mg', 'cy', 'wh' } do
  C[colour] = function(x) return '\x1B[0;'..(i+29)..'m'..x end
  C[colour:upper()] = function(x) return '\x1B[1;'..(i+29)..'m'..x end
end

local beings = require 'beings'

local hit = C.RD '*'
local fire = C.YL '!'
local die = C.RD '%'

local function write(text, file)
  assert(io.open(file, 'w')):write(text)
end

local function write_effects(type, name, face, hit, fire, die)
  write(face, type..'/'..name..'/act')
  write(hit..face..hit, type..'/'..name..'/hit')
  write(fire..face..fire, type..'/'..name..'/fire')
  write(die..face..die, type..'/'..name..'/die')
end

-- Symbolic effects with colours, for use in the tty.
for name,def in pairs(beings) do
  local face = C[def.colour](def.face)
  write_effects('symbolic', name, face, hit, fire, die)
end

write(C.yl '+', 'symbolic/door/close')
write(C.yl '/', 'symbolic/door/open')
write(C.CY '*', 'symbolic/teleporter')
write(C.YL '*', 'symbolic/explosion')
write(C.WH '*', 'symbolic/gunfire')

-- Symbolic effects without colours, for use in SDL.
for name,def in pairs(beings) do
  write_effects('plain-symbolic', name, def.face, '*', '!', '%')
end

write('+', 'plain-symbolic/door/close')
write('/', 'plain-symbolic/door/open')
write('*', 'plain-symbolic/teleporter')
write('*', 'plain-symbolic/explosion')
write('*', 'plain-symbolic/gunfire')
