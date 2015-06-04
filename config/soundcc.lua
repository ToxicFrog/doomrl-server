if DeafMode ~= 'symbolic' and DeafMode ~= 'descriptive' then
  DeafMode = 'raw'
end

Sound = {
  door = {
    open  = 'cc/'..DeafMode..'/door/open';
    close = 'cc/'..DeafMode..'/door/close';
  };
  teleport = {
    use   = 'cc/'..DeafMode..'/teleporter';
  };
  explode = 'cc/'..DeafMode..'/explosion';
  fire    = 'cc/'..DeafMode..'/gunfire';
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
  sounds.die  = 'cc/'..DeafMode..'/'..name..'/die'
  sounds.act  = 'cc/'..DeafMode..'/'..name..'/act'
  sounds.hit = 'cc/'..DeafMode..'/'..name..'/hit'
  sounds.fire = 'cc/'..DeafMode..'/'..name..'/fire'
  sounds.hoof = 'cc/TICK'
  Sound[name] = sounds
end
