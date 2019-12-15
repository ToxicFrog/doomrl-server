-- Whether to allow high-ASCII signs. Set to false if you see weird signs
-- on the screen. Windows users may want to enable this.
AllowHighAscii   = false

-- Specifies wether items in inventory and equipment should be colored
ColoredInventory = true

-- Menu styles can be LETTER for letter choince only menus, CHOICE for only
-- arrow selection or HYBRID for both. Note that additional commands (like
-- BACKSPACE for in-menu drop and TAB for swap) wont work in the LETTER mode.
InvMenuStyle     = "HYBRID"
EqMenuStyle      = "HYBRID"
HelpMenuStyle    = "HYBRID"

-- Setting to true will skip the intro
SkipIntro        = false

-- Setting to true will remove the bloodslide effect
NoBloodSlides    = false

-- Setting to true will remove the flashing effect
NoFlashing       = false

-- Setting to true will make the run command not stop on items
RunOverItems     = false

-- Setting to true will turn on enhancements for blind people playing
-- DoomRL using a screen reader. Yes, some do.
BlindMode        = false

-- Setting to true will turn on enhancements for colorblind people.
ColorBlindMode   = false

-- Configure closed caption support.
-- "sfx" plays sounds (in the browser) but displays nothing.
-- "fancy" shows you monster symbols with colour.
-- "fancy+sfx" combines both, playing sounds and showing symbols.
-- "plain" shows you monster symbols with no colour.
-- "raw" shows you raw event names, and is mostly useful for debugging.
-- "default" is server-specific but was "fancy+sfx" when this file was created.
ClosedCaptions = true
ClosedCaptionStyle = 'default'

-- Control how Nightmare enemies ("nightmare ___" and "elite ___") are handled
-- by the closed captions.
-- "full" gives them their own closed caption data.
-- "limited" re-uses the CC data for non-nightmare versions, so you can tell
-- that they're there but can't distinguish them from normal enemies.
-- "none" disables CC for nightmare enemies entirely, making them silent.
NightmareClosedCaptionStyle = "full"

-- Setting to true will make old messages disappear from the screen
-- (useful in BlindMode)
ClearMessages    = false

-- Setting to true will skip name entry procedure and choose a random name
-- instead
AlwaysRandomName = false

-- Setting this to anything except "" will always use that as the name.
-- Warning - no error checking, so don't use too long names, or especially
-- the "@" sign (it's a control char). This setting overrides the one above!
AlwaysName       = ""

-- Setting to false will prevent DoomRL from waiting for confirmation
-- when too many messages are printed in a turn. Usefull for Speedrunning.
MorePrompt       = true

-- Setting to true will make the game wait for an enter/space key if
-- trying to fire an empty weapon.
EmptyConfirm     = false

-- Controls whether gameplay hints appear on the intro level. Once you learn
-- to use the game, you can safely turn it off!
Hints            = true

-- Sets the delay between steps when running. Value is in milliseconds. Set to
-- 0 for no delay.
RunDelay         = 20

-- Handles what should be done in case of trying to unwield an item when
-- inventory is full : if set to false will ask the player if they want to drop
-- it. If set to true will drop it without questions.
InvFullDrop      = false

-- Messages held in the message buffer.
MessageBuffer    = 100

-- Sets wether message coloring will be enabled. Needs [messages] section.
MessageColoring  = true

-- Defines the maximum repeat for the run command. Setting it to larger than 80
-- basically means no limit.
MaxRun           = 100

-- Defines the maximum repeat for the run command when waiting.
MaxWait          = 20

-- Sets the color of intuition effect for beings
IntuitionColor   = LIGHTMAGENTA

-- Sets the char of intuition effect for beings
IntuitionChar    = "*"

-- Message coloring system. Works only if MessageColoring
-- variable is set to true. Use basic color names available in
-- colors.lua.
-- As for the string, it's case sensitive, but you may use
-- the wildcard characters * and ?.

-- Unsure how these work and want to fiddle with them?
-- Head over to http://forum.chaosforge.org/ for more info.
Messages = {
  ["Warning!*"]                   = RED,
  ["Your * destroyed!"]             = RED,
  ["You die*"]                      = RED,
  ["Your * damaged!"]               = BROWN,
  ["You feel relatively safe now."] = BLUE
}
