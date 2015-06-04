Sound = {
  door = {
    open  = 'cc/door/open';
    close = 'cc/door/close';
  };
  teleport = {
    use   = 'cc/teleporter';
  };
  explode = 'cc/explosion';
  fire    = 'cc/gunfire';
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
  sounds.die  = 'cc/'..name..'/die'
  sounds.act  = 'cc/'..name..'/act'
  sounds.hit = 'cc/'..name..'/hit'
  sounds.hoof = 'cc/TICK'
  Sound[name] = sounds
end
