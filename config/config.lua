
-- COMMAND_* constants
dofile "commands.lua"
-- Default keybindings
dofile "defaultcontrols.lua"

-- user-defined settings
dofile "colours.lua"
dofile "controls.lua"
dofile "user.lua"

----------------------------------------------------------------------
-- Master settings that are meant to override the user-specified ones.
----------------------------------------------------------------------

-- QuickKey and numeric movement support, if the user asked for it in controls.lua
dofile "quickkeys.lua"

-- Graphics mode. Can be CONSOLE for raw console, or TILES for graphical
-- tiles. Overriden by -graphics and -console command line parameters.
Graphics = "CONSOLE"

-- Sound engine, by default is FMOD on Windows, SDL on *nix. To use SDL on
-- Windows you'll need SDL_mixer.dll and smpeg.dll from SDL_mixer website.
-- For using FMOD on *nix systems you'll need the proper packages.
-- Possible values are FMOD, SDL, NONE, DEFAULT
SoundEngine = "NONE"

-- Setting to false will turn off music during gameplay
GameMusic        = false

-- Setting to false will turn off sounds during gameplay
GameSound        = false

-- Setting to false will turn off Menu change/select sound
MenuSound        = false

-- If set to true, pickup sound will be used for quickkeys and weapon
-- swapping.
SoundEquipPickup = false

-- If set to true will archive EVERY mortem.txt produced in the mortem subfolder.
-- The amount of files can get big after a while :)
MortemArchive    = true

-- Sets the amount of player.wad backups. Set 0 to turn off. At most one backup
-- is held for a given day.
PlayerBackups    = 1

-- Sets the amount of score.wad backups. Set 0 to turn off.  At most one backup
-- is held for a given day.
ScoreBackups     = 1

-- If set to false DoomRL will quit on death and quitting. Normally it will go back
-- to the main menu.
MenuReturn       = false

-- Mortem and screenshot timestamp format
-- Format : http://www.freepascal.org/docs-html/rtl/sysutils/formatchars.html
-- note that / and : will be converted to "-" due to filesystem issues
TimeStamp        = "yyyy-mm-dd hh-nn-ss"

-- Controls whether the game will attempt to save the game on crash, set to false
-- to turn this off
SaveOnCrash      = true

-- This is the global internet connection switch, allowing DoomRL
-- to use internet connection features. Think twice before disabling
-- it, or you'll loose the features listed below and MOTD and ModServer
-- support!
NetworkConnection = false

-- Should DoomRL check if there's a new version at runtime. If
-- NetworkConnection is set to true this check is made regardless,
-- but there will be no alert if set to false.
VersionCheck = false

-- Should DoomRL check if there's a new BETA version at runtime. If
-- NetworkConnection is set to true this check is made regardless,
-- but there will be no alert if set to false. BETA versions are only
-- available to Supporters, but why not hop in and join the fun?
-- By default it's set to VERSION_BETA which is true for beta releases
-- and false for stable releases. Set to true, to get notified of the
-- next BETA batch!
BetaCheck = VERSION_BETA

-- Should DoomRL check for other alerts. Sometimes we will want to
-- point you out to a major ChaosForge release or news flash. This feature
-- will not be abused, and each alert will be displayed only once, so
-- please consider leaving this set to true! :)
AlertCheck = false

-- DoomRL by default uses it's own mod server, where we host only screened
-- mods from the DoomRL community. A day may come when there will be an
-- unofficial server, for example for mods in testing. You can specify it
-- here. Note that this overrides the default server.
CustomModServer = ''

--------------------------------------------------------------------------------
-- Settings irrelevant to server operation, moved here and kept at their default
-- values to keep clutter out of the user config file.
------------------------------------------------------

-- SDL sound only options. See SDL_mixer manual on what to put here if
-- defaults don't get you working audio. Format needs to be decoded because
-- Lua doesn't support hex notation.
SDLMixerFreq      = 44100
SDLMixerFormat    = 32784
SDLMixerChunkSize = 1024

-- Windows and GFX mode only:
-- Set to false to turn off the Fullscreen query at run time. If false you
-- can use StartFullscreen to control fullscreen at startup.
FullscreenQuery  = true

-- whether to start in fullscreen mode, use ALT-Enter to toggle, only
-- used when FullscreenQuery is set to false
StartFullscreen  = false

-- Windowed sizes
WindowedWidth       = 800
WindowedHeight      = 600
-- Multiplication values of font and tile display - use at most 2
WindowedFontMult    = 1
WindowedTileMult    = 1
-- minimap size multiplication, set to 0 to remove minimap, -1 is auto
-- choice based on resolution
WindowedMiniMapSize = -1

-- Fullscreen resolution sizes
-- -1 means auto-detection of screen size, and fontmult and tilemult and
-- minimap based on it
FullscreenWidth       = -1
FullscreenHeight      = -1
FullscreenFontMult    = -1
FullscreenTileMult    = -1
FullscreenMiniMapSize = -1

-- Music volume in the range of 0..25
MusicVolume      = 12

-- Sound volume in the range of 0..25
SoundVolume      = 20

-- Windows only - disables Ctrl-C/Ctrl-Break closing of program.
-- true by default.
LockBreak        = true

-- Windows only - Disables closing of DoomRL by console close button.
-- true by default.
LockClose        = true

-- At the end so that it can override previous sound settings if the user turned
-- closed captions on.
dofile "soundcc.lua"
