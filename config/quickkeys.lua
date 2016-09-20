-- Alternate movement bindings using the number keys, for numpad usage over telnet.
if BindMovementToNumKeys then
  Keybindings["8"] = COMMAND_WALKNORTH
  Keybindings["9"] = COMMAND_WALKNE
  Keybindings["6"] = COMMAND_WALKEAST
  Keybindings["3"] = COMMAND_WALKSE
  Keybindings["2"] = COMMAND_WALKSOUTH
  Keybindings["1"] = COMMAND_WALKSW
  Keybindings["4"] = COMMAND_WALKWEST
  Keybindings["7"] = COMMAND_WALKNW
  Keybindings["5"] = COMMAND_WAIT
end

-- List of keys to set up as quickkeys.
local QuickKeys = {}
if BindQuickKeysTo == 'num-keys' then
  QuickKeys = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' }
elseif BindQuickKeysTo == 'f-keys' then
  QuickKeys = { 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F11', 'F12' }
end

-- List of weapons to bind to those keys.
local QuickKeyWeapons = {
  'chainsaw', 'knife', 'pistol', 'shotgun', 'ashotgun',
  'dshotgun', 'chaingun', 'bazooka', 'plasma', 'bfg9000'
}
-- Given a weapon name, return a QuickKey function for it.
local function MakeQuickKey(weapon)
  return function() command.quick_weapon(weapon) end
end

---- Begin QuickKey category support. ----

-- QuickKey weapon categories. Each key cycles through the corresponding category.
local QuickKeyCategories = {
  { name = 'melee weapons';
    'knife', 'chainsaw', 'ubutcher', 'usubtle', 'umjoll', 'spear', 'uscythe' };
  { name = 'pistols';
    'pistol', 'ucpistol', 'ublaster', 'utrigun', 'uberetta', 'ujackal' };
  { name = 'shotguns';
    'shotgun', 'dshotgun', 'ashotgun', 'udshotgun', 'uashotgun', 'upshotgun', 'usjack', 'ufshotgun' };
  { name = 'rapid-fire weapons';
    'chaingun', 'uminigun', 'plasma', 'unplasma', 'ulaser', 'umega' };
  { name = 'explosive weapons';
    'bazooka', 'umbazooka', 'unapalm', 'urbazooka' };
  { name = 'BFGs';
    'bfg9000', 'unbfg9000', 'ubfg10k' };
  { name = 'exotic weapons';
    'utristar', 'utrans', 'urailgun', 'uacid', 'unullpointer' };
}

-- Get the last complete log message. Seeks backwards in the log until it either
-- runs out of logging or finds an empty line.
local function GetLastFullMessage()
  local n,msg = 0,''
  repeat
    msg = ui.msg_history(n) .. msg
    n = n+1
  until ui.msg_history(n) == nil or not ui.msg_history(n):match('%S')

  return msg
end

-- Attempt to equip a weapon and read the log to figure out if we succeeded or not.
-- Also attempts to clean up the log after itself on success.
local function TryEquip(weapon)
  ui.msg_clear()
  command.quick_weapon(weapon)
  local msg = GetLastFullMessage()
  local success_msg = msg:match("You prepare the .-[.!] ")
    or msg:match("You already have the .-[.!] ")
    or msg:match("You swap your weapons.-[.!] ")

  if not success_msg then return false end
  if msg ~= success_msg then
    -- This means that there were additional messages appended to the equip message,
    -- almost certainly "there is a %s lying here". Due to a bug in DoomRL, this
    -- will get appended twice, once now and once when we return from the key handler.
    -- So, we get rid of it here so it only appears once.
    ui.msg_clear()
    ui.msg(success_msg)
  end
  return true
end

-- QuickKey function builder for categories. Some ugly hacks in here (repeatedly
-- clearing the log, reading the log messages to figure out what happened)
-- because command.quick_weapon() doesn't return a value indicating whether
-- we successfully equipped a thing the way command.use_item does.
local current_category
local function MakeQuickKeyForCategory(category)
  local index = 1
  local max = #category
  local function inc() index = index % #category + 1;
    return index end
  return function()
    -- Player probably already has category[index] equipped.
    -- Skip to the next weapon.
    if current_category == category then inc() end

    -- Search for the first weapon in this category that the player has.
    local start = index
    repeat
      if TryEquip(category[index]) then
        current_category = category
        return
      end

      -- Proceed to the next weapon. Stop if we've looped all the way around
      -- to the weapon we started with.
    until inc() == start

    -- We ran out of weapons to try. Clear any lingering "you don't have the" messages.
    ui.msg_clear()
    ui.msg("You don't have any "..category.name..".")
  end
end

if QuickKeysUseCategories then
  MakeQuickKey = MakeQuickKeyForCategory
  QuickKeyWeapons = QuickKeyCategories
end

for i,key in ipairs(QuickKeys) do
  if QuickKeyWeapons[i] then
    Keybindings[key] = MakeQuickKey(QuickKeyWeapons[i])
  end
end
