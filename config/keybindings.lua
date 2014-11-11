Keybindings = {
	["LEFT"]         = COMMAND_WALKWEST,
	["RIGHT"]        = COMMAND_WALKEAST,
	["UP"]           = COMMAND_WALKNORTH,
	["DOWN"]         = COMMAND_WALKSOUTH,
	["PGUP"]         = COMMAND_WALKNE,
	["PGDOWN"]       = COMMAND_WALKSE,
	["HOME"]         = COMMAND_WALKNW,
	["END"]          = COMMAND_WALKSW,
	["ESCAPE"]       = COMMAND_ESCAPE,
	["CENTER"]       = COMMAND_WAIT,
	["PERIOD"]       = COMMAND_WAIT,
	["BEGIN"]        = COMMAND_WAIT,
	["ENTER"]        = COMMAND_OK,
	["M"]            = COMMAND_MORE,
	["SHIFT+PERIOD"] = COMMAND_ENTER,
	["SHIFT+U"]      = COMMAND_UNLOAD,
	["G"]            = COMMAND_PICKUP,
	["D"]            = COMMAND_DROP,
	["I"]            = COMMAND_INVENTORY,
	["E"]            = COMMAND_EQUIPMENT,
	["O"]            = COMMAND_OPEN,
	["C"]            = COMMAND_CLOSE,
	["L"]            = COMMAND_LOOK,
	-- GRIDTOGGLE does nothing in console mode, so we bind space to be an alternate
	-- ESCAPE instead. This is especially convenient because DoomRL has a long-
	-- standing bug where you have to double-tap Esc in console mode before it
	-- will register.
	-- ["SPACE"]        = COMMAND_GRIDTOGGLE,
	["SPACE"]        = COMMAND_ESCAPE,
	["F"]            = COMMAND_FIRE,    -- function() command.fire() end,
	["SHIFT+F"]      = COMMAND_ALTFIRE, -- function() command.fire( true ) end,
	["R"]            = function() command.reload() end,
	["SHIFT+R"]      = function() command.reload( true ) end,
	["U"]            = COMMAND_USE,
	["SHIFT+Q"]      = function() command.quit() end,
	["SHIFT+SLASH"]  = function() command.help() end,
	["SHIFT+2"]      = COMMAND_PLAYERINFO,
	["SHIFT+S"]      = COMMAND_SAVE,
	TAB              = COMMAND_TACTIC,
	["COMMA"]        = COMMAND_RUNMODE,
	["Z"]            = COMMAND_SWAPWEAPON,
--	F10       = function() command.screenshot() end, -- currently hardcoded
--	F9        = function() command.screenshot( true ) end,-- currently hardcoded
	["T"]            = COMMAND_TRAITS,
	["SHIFT+9"]      = COMMAND_SOUNDTOGGLE,
	["SHIFT+0"]      = COMMAND_MUSICTOGGLE,
	["SHIFT+P"]      = function() command.messages() end,
	["SHIFT+A"]      = function() command.assemblies() end,
	-- Commands for blind mode:
	["X"]            = COMMAND_EXAMINENPC,
	["SHIFT+X"]      = COMMAND_EXAMINEITEM,
	-- QuickKeys
	["0"]     = function() command.quick_weapon('chainsaw') end,
	["1"]     = function() command.quick_weapon('knife') end,
	["2"]     = function() command.quick_weapon('pistol') end,
	["3"]     = function() command.quick_weapon('shotgun') end,
	["4"]     = function() command.quick_weapon('ashotgun') end,
	["5"]     = function() command.quick_weapon('dshotgun') end,
	["6"]     = function() command.quick_weapon('chaingun') end,
	["7"]     = function() command.quick_weapon('bazooka') end,
	["8"]     = function() command.quick_weapon('plasma') end,
	["9"]     = function() command.quick_weapon('bfg9000') end,

	-- Alternate keypad controls. These require you to have numlock ON, and disable
	-- the fast weapon switch keys above. The advantage is that it means you can
	-- now use numpad 5 as a "wait" command.
	["8"]     = COMMAND_WALKNORTH,
	["9"]     = COMMAND_WALKNE,
	["6"]     = COMMAND_WALKEAST,
	["3"]     = COMMAND_WALKSE,
	["2"]     = COMMAND_WALKSOUTH,
	["1"]     = COMMAND_WALKSW,
	["4"]     = COMMAND_WALKWEST,
	["7"]     = COMMAND_WALKNW,
	["5"]     = COMMAND_WAIT,

	-- Example of complex quickkeys
	["SHIFT+N"]    = function()
					if not command.use_item("smed") then
						ui.msg("No small medpacks left!")
					end
				end,
	["SHIFT+M"]    = function()
					if not command.use_item("lmed") then
						ui.msg("No large medpacks left!")
					end
				end,
}
