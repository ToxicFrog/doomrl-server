if not ClosedCaptions then return end

-- Set default values
ClosedCaptionStyle = ClosedCaptionStyle or 'auto'
NightmareClosedCaptionStyle = NightmareClosedCaptionStyle or 'full'

-- Supported styles. Edit this list if you're adding a new style, or an alias
-- for an existing one.
local styles = {
  -- Included styles
  fancy = 'fancy';
  plain = 'plain';
  raw = 'raw';
  sfx = 'sfx';
  ['fancy+sfx'] = 'fancy+sfx';
  -- Aliases
  auto = Graphics == 'CONSOLE' and 'fancy+sfx' or 'plain';
  default = 'fancy+sfx';
}

local style = styles[ClosedCaptionStyle] or styles.default

-- Override sound engine settings.
SoundEngine = "SDL"
if MenuSound == nil then MenuSound = true end
if GameSound == nil then GameSound = true end
if GameMusic == nil then GameMusic = true end

dofile('cc/'..style..'/init.lua')
