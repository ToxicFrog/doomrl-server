COMMAND_WALKNORTH         = 2;
COMMAND_WALKSOUTH         = 3;
COMMAND_WALKEAST          = 4;
COMMAND_WALKWEST          = 5;
COMMAND_WALKNE            = 6;
COMMAND_WALKSE            = 7;
COMMAND_WALKNW            = 8;
COMMAND_WALKSW            = 9;
COMMAND_WAIT              = 10;
COMMAND_ESCAPE            = 11;
COMMAND_OK                = 12;
COMMAND_ENTER             = 13;
COMMAND_UNLOAD            = 14;
COMMAND_PICKUP            = 15;
COMMAND_DROP              = 16;
COMMAND_INVENTORY         = 17;
COMMAND_EQUIPMENT         = 18;
COMMAND_OPEN              = 19;
COMMAND_CLOSE             = 20;
COMMAND_LOOK              = 21;
COMMAND_ALTFIRE           = 23;
COMMAND_FIRE              = 24;
COMMAND_USE               = 25;
COMMAND_PLAYERINFO        = 26;
COMMAND_SAVE              = 27;
COMMAND_TACTIC            = 28;
COMMAND_RUNMODE           = 29;
COMMAND_MORE              = 31;
COMMAND_EXAMINENPC        = 32;
COMMAND_EXAMINEITEM       = 33;
COMMAND_SWAPWEAPON        = 34;
COMMAND_TRAITS            = 39;
COMMAND_GRIDTOGGLE        = 40;

COMMAND_SOUNDTOGGLE       = 86;
COMMAND_MUSICTOGGLE       = 87;

-- Command aliases not built into DoomRL, but provided here for player convenience.
function COMMAND_RELOAD() return command.reload() end
function COMMAND_SPECIAL_RELOAD() return command.reload(true) end
function COMMAND_QUIT() return command.quit() end
function COMMAND_HELP() return command.help() end
function COMMAND_MESSAGES() return command.messages() end
function COMMAND_ASSEMBLIES() return command.assemblies() end
