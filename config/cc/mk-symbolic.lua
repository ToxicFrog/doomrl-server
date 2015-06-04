local C = {}
for i,colour in ipairs { 'bk', 'rd', 'gr', 'yl', 'bl', 'mg', 'cy', 'wh' } do
  C[colour] = function(x) return '\x1B[0;'..(i+29)..'m'..x end
  C[colour:upper()] = function(x) return '\x1B[1;'..(i+29)..'m'..x end
end

local symbols = {
  former      = C.wh 'h';
  sergeant    = C.BK 'h';
  captain     = C.RD 'h';
  commando    = C.BL 'h';
  imp         = C.yl 'i';
  demon       = C.MG 'c';
  lostsoul    = C.YL 's';
  pain        = C.yl 'O';
  cacodemon   = C.RD 'O';
  arachno     = C.YL 'A';
  knight      = C.yl 'B';
  baron       = C.MG 'B';
  mancubus    = C.yl 'M';
  revenant    = C.WH 'R';
  arch        = C.YL 'V';
  bruiser     = C.RD 'B';
  cyberdemon  = C.yl 'C';
  angel       = C.rd 'A';
  mastermind  = C.WH 'M';
  jc          = C.BL '@';
}

local hit = C.RD '*'
local die = C.RD '%'
local fire = C.YL '!'

local function write(text, file)
  assert(io.open(file, 'w')):write(text)
end

for enemy,symbol in pairs(symbols) do
  write(symbol, 'cc/symbolic/'..enemy..'/act')
  write(hit..symbol..hit, 'cc/symbolic/'..enemy..'/hit')
  write(fire..symbol..fire, 'cc/symbolic/'..enemy..'/fire')
  write(die..symbol..die, 'cc/symbolic/'..enemy..'/die')
end

write(C.yl '+', 'cc/symbolic/door/close')
write(C.yl '/', 'cc/symbolic/door/open')
write(C.CY '*', 'cc/symbolic/teleporter')
write(C.YL '*', 'cc/symbolic/explosion')
write(C.WH '*', 'cc/symbolic/gunfire')
