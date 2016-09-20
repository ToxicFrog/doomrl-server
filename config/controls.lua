-- Use 12346789 for movement and 5 to wait in place. This lets you play using
-- the number pad even if numlock is on, and use 5 to wait, at the cost of not
-- being able to use the number keys to switch weapons, since DoomRL can't tell
-- the difference between the normal number keys and the numpad in tty mode.
-- The default is on
BindMovementToNumKeys = true

-- Automatically set up weapon quickkeys.
-- If set to 'num-keys', it'll set up the same bindings as stock DoomRL.
-- If set to 'f-keys', it'll bind the quickkeys to F1-F8, F11, and F12 (F9 and
-- F10 are hard-coded to "take screenshot").
-- Any other value disables automatic QuickKey binding.
-- The default is to use the f-keys if BindMovementToNumKeys is on, and use the
-- num-keys otherwise.
BindQuickKeysTo = BindMovementToNumKeys and 'f-keys' or 'num-keys'

-- Set up quickkeys to select weapon categories rather than individual weapons.
-- If you set this option, rather than each key corresponding to a single weapon,
-- it corresponds to a group of weapons. Pressing the key once will select the
-- last weapon of that category you used; continuing to press will cycle through
-- that category.
-- Note that due to limitations in the DoomRL quickkey API, this will generate
-- a lot of log spam every time you use it. It'll be hidden on the main screen
-- but will show up in the full (shift-P) log.
-- The categories are:
-- 1 - melee
-- 2 - pistols
-- 3 - shotguns
-- 4 - rapid fire
-- 5 - explosive
-- 6 - BFGs
-- 7 - miscellaneous
QuickKeysUseCategories = true

-- Add any keybind overrides you want to this file.
-- For example, to swap z and x:
-- bind {
--	 X = COMMAND_SWAPWEAPON;
--   Z = COMMAND_EXAMINENPC;
-- }

-- To unbind a key, use unbind():
-- unbind('SHIFT+M', 'SHIFT+N')
