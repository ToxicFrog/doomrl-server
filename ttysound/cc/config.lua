if not ClosedCaptions then return end

-- Set default values
ClosedCaptionStyle = ClosedCaptionStyle or 'auto'
NightmareClosedCaptionStyle = NightmareClosedCaptionStyle or 'full'

-- Errors don't get propagated by DoomRL dofile(), so we explicitly print them
-- here.
local function CHECK(val, msg)
  if val then return end
  print(msg)
  error(msg)
end

-- Supported styles. Edit this list if you're adding a new style, or an alias
-- for an existing one.
local styles = {
  auto = Graphics == 'CONSOLE' and 'fancy' or 'plain';
  default = 'fancy';
  fancy = 'fancy';
  plain = 'plain';
  raw = 'raw';
}

local style = styles[ClosedCaptionStyle]
CHECK(style, "Unknown ClosedCaptionStyle: " .. tostring(ClosedCaptionStyle))

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

-- Load beings table and generate sound map for beings.
function createSoundMapForBeing(style, name, def)
  if def.nightmare_of then
    if NightmareClosedCaptionStyle == "none" then
      return nil
    elseif NightmareClosedCaptionStyle == "limited" then
      name = def.nightmare_of
    elseif NightmareClosedCaptionStyle == "full" then
      -- pass
    else
      CHECK(false, "Unknown NightmareClosedCaptionStyle: " .. tostring(NightmareClosedCaptionStyle))
    end
  end

  return {
    die  = 'cc/'..style..'/'..name..'/die';
    act  = 'cc/'..style..'/'..name..'/act';
    hit  = 'cc/'..style..'/'..name..'/hit';
    fire = 'cc/'..style..'/'..name..'/fire';
    hoof = 'cc/TICK';
  }
end

for name,def in pairs(loadfile('cc/beings.lua')()) do
  Sound[name] = createSoundMapForBeing(style, name, def)
end
