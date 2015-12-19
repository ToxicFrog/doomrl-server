-- Supported styles. Edit this list if you're adding a new style, or an alias
-- for an existing one.
local styles = {
  default = 'symbolic';
  symbolic = 'symbolic';
  raw = 'raw';
  descriptive = 'descriptive';
}

local style = styles[DeafMode]

-- Unrecognized DeafMode will result in it being set to nil. In that case
-- (or if explicitly set to false), early return without changing any settings.
if not style then return end

-- Override sound engine settings.
SoundEngine = "SDL"
GameSound = true
GameMusic = false
MenuSound = false

-- Override sound effects map.
Sound = {
  door = {
    open  = 'cc/'..style..'/door/open';
    close = 'cc/'..style..'/door/close';
  };
  teleport = {
    use   = 'cc/'..style..'/teleporter';
  };
  explode = 'cc/'..style..'/explosion';
  fire    = 'cc/'..style..'/gunfire';
  pickup  = 'cc/TICK';
  reload  = 'cc/TICK';
  powerup = 'cc/TICK';
  barrel = {
  	move = 'cc/TICK';
  	movefail = 'cc/TICK';
  };
  barrela = {
  	move = 'cc/TICK';
  	movefail = 'cc/TICK';
  };
  barreln = {
  	move = 'cc/TICK';
  	movefail = 'cc/TICK';
  };
}

local enemies = {
  'former', 'sergeant', 'captain', 'commando',
  'imp', 'demon', 'lostsoul', 'pain',
  'cacodemon', 'arachno', 'knight', 'baron',
  'mancubus', 'revenant', 'arch',
  -- bosses
  'bruiser', 'cyberdemon', 'angel', 'mastermind', 'jc',
}

for i=1,#enemies do
  local name = enemies[i]
  local sounds = {}
  sounds.die  = 'cc/'..style..'/'..name..'/die'
  sounds.act  = 'cc/'..style..'/'..name..'/act'
  sounds.hit = 'cc/'..style..'/'..name..'/hit'
  sounds.fire = 'cc/'..style..'/'..name..'/fire'
  sounds.hoof = 'cc/TICK'
  Sound[name] = sounds
end
