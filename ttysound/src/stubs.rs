////
//// Stubbed out functions.
//// These are present so that doomrl's dlopen() finds them when it asks, but
//// if any of them are called they will emit an error message and abort.
////

extern crate libc;

use libc::exit;
use std::io::Write;
use std::io::stderr;
use std::ptr;

use types::*;

fn die(msg: &str) {
  writeln!(&mut stderr(), "FATAL: {}", msg)
    .ok().expect("Error writing error message :(");
  unsafe { exit(1) }
}

////
//// Sample functions ////
////

#[no_mangle]
pub extern fn Mix_QuickLoad_WAV(mem: *const u8) -> *const libc::c_void {
  die("Mix_QuickLoad_WAV not implemented.");
  ptr::null()
}
#[no_mangle]
pub extern fn Mix_VolumeChunk(chunk: *const Mix_Chunk, volume: i32) -> i32 {
  die("Mix_VolumeChunk not implemented.");
  volume
}

////
//// Channel functions ////
////

#[no_mangle]
pub extern fn Mix_AllocateChannels(channels: i32) -> i32 {
  die("Mix_AllocateChannels not implemented!");
  channels
}

#[no_mangle]
pub extern fn Mix_FadeInChannelTimed(channel: i32,
                                     chunk: *const Mix_Chunk,
                                     loops: i32,
                                     ms: i32,
                                     ticks: i32) -> i32 {
  die("Mix_FadeInChannelTimed not implemented.");
  0
}

#[no_mangle]
pub extern fn Mix_Pause(channel: i32) -> () {
  die("Mix_Pause not implemented.");
}
#[no_mangle]
pub extern fn Mix_Resume(channel: i32) -> () {
  die("Mix_Resume not implemented.");
}

#[no_mangle]
pub extern fn Mix_HaltChannel(channel: i32) -> i32 {
  die("Mix_HaltChannel not implemented.");
  0
}
#[no_mangle]
pub extern fn Mix_ExpireChannel(channel: i32, ticks: i32) -> i32 {
  die("Mix_ExpireChannel not implemented.");
  1
}
#[no_mangle]
pub extern fn Mix_FadeOutChannel(channel: i32, ms: i32) -> i32 {
  die("Mix_FadeOutChannel not implemented.");
  1
}
#[no_mangle]
pub extern fn Mix_ChannelFinished(f: *const u8) -> () {
  die("Mix_ChannelFinished not implemented.");
}

#[no_mangle]
pub extern fn Mix_Paused(channel: i32) -> i32 {
  die("Mix_Paused not implemented.");
  0
}
#[no_mangle]
pub extern fn Mix_Playing(channel: i32) -> i32 {
  die("Mix_Playing not implemented.");
  0
}
#[no_mangle]
pub extern fn Mix_FadingChannel(channel: i32) -> i32 {
  die("Mix_FadingChannel not implemented.");
  0 // MIX_NO_FADING
}
#[no_mangle]
pub extern fn Mix_GetChunk(channel: i32) -> *const Mix_Chunk {
  die("Mix_ not implemented.");
  ptr::null()
}

////
//// Music functions ////
////

#[repr(C)]
pub struct Mix_Music;

#[no_mangle]
pub extern fn Mix_LoadMUS(file: *const libc::c_char) -> *const Mix_Music {
  die("LoadMUS not implemented.");
  ptr::null()
}
#[no_mangle]
pub extern fn Mix_LoadMUS_RW(src: *const SDL_RWops) -> *const Mix_Music {
  die("LoadMUS_RW not implemented.");
  ptr::null()
}

#[no_mangle]
pub extern fn Mix_PlayMusic(music: *const Mix_Music, loops: i32) -> i32 {
  die("Mix_PlayMusic not implemented.");
  0
}
#[no_mangle]
pub extern fn Mix_FadeInMusic(music: *const Mix_Music, loops: i32, ms: i32) -> i32 {
  die("Mix_FadeInMusic not implemented.");
  0
}
#[no_mangle]
pub extern fn Mix_HookMusic(f: *const u8, arg: *const u8) -> () {
  die("Mix_HookMusic not implemented.");
}

#[no_mangle]
pub extern fn Mix_VolumeMusic(volume: i32) -> i32 {
  //die("Mix_VolumeMusic not implemented.");
  volume
}
#[no_mangle]
pub extern fn Mix_PauseMusic() -> () {
  die("Mix_PauseMusic not implemented.");
}
#[no_mangle]
pub extern fn Mix_ResumeMusic() -> () {
  die("Mix_ResumeMusic not implemented.");
}
#[no_mangle]
pub extern fn Mix_RewindMusic() -> () {
  die("Mix_RewindMusic not implemented.");
}
#[no_mangle]
pub extern fn Mix_SetMusicPosition(position: f64) -> i32 {
  die("Mix_SetMusicPosition not implemented.");
  0
}
#[no_mangle]
pub extern fn Mix_SetMusicCMD(command: *const libc::c_char) -> i32 {
  die("Mix_SetMusicCMD not implemented.");
  0
}

#[no_mangle]
pub extern fn Mix_HaltMusic() -> i32 {
  die("Mix_HaltMusic not implemented.");
  0
}
#[no_mangle]
pub extern fn Mix_FadeOutMusic(ms: i32) -> i32 {
  die("Mix_FadeOutMusic not implemented.");
  1
}
#[no_mangle]
pub extern fn Mix_HookMusicFinished(f: *const u8) -> () {
  die("Mix_HookMusicFinished not implemented.");
}

#[no_mangle]
pub extern fn Mix_GetMusicType(music: *const Mix_Music) -> i32 {
  die("Mix_GetMusicType not implemented!");
  0 // MIX_NONE
}
#[no_mangle]
pub extern fn Mix_PlayingMusic() -> i32 {
  die("Mix_PlayingMusic not implemented!");
  0
}
#[no_mangle]
pub extern fn Mix_PausedMusic() -> i32 {
  die("Mix_PausedMusic not implemented!");
  0
}
#[no_mangle]
pub extern fn Mix_FadingMusic() -> i32 {
  die("Mix_FadingMusic not implemented!");
  0 // MIX_NO_FADING
}
#[no_mangle]
pub extern fn Mix_GetMusicHookData() -> *const u8 {
  die("Mix_GetMusicHookData not implemented!");
  ptr::null() // TODO: do we need to DTRT here?
}

#[no_mangle]
pub extern fn Mix_FreeMusic(chunk: *const Mix_Music) -> () {
  die("Mix_FreeMusic not implemented.");
}

////
//// Grouping functions ////
////

#[no_mangle]
pub extern fn Mix_ReserveChannels(num: i32) -> i32 {
  die("Mix_ReserveChannels not implemented!");
  num
}

#[no_mangle]
pub extern fn Mix_GroupChannel(which: i32, tag: i32) -> i32 {
  die("Mix_GroupChannel not implemented!");
  1
}
#[no_mangle]
pub extern fn Mix_GroupChannels(from: i32, to: i32, tag: i32) -> i32 {
  die("Mix_GroupChannels not implemented!");
  to - from + 1
}

#[no_mangle]
pub extern fn Mix_GroupCount(tag: i32) -> i32 {
  die("Mix_GroupCount not implemented!");
  0
}
#[no_mangle]
pub extern fn Mix_GroupAvailable(tag: i32) -> i32 {
  die("Mix_GroupAvailable not implemented!");
  0
}
#[no_mangle]
pub extern fn Mix_GroupOldest(tag: i32) -> i32 {
  die("Mix_GroupOldest not implemented!");
  0
}
#[no_mangle]
pub extern fn Mix_GroupNewer(tag: i32) -> i32 {
  die("Mix_GroupNewer not implemented!");
  0
}

#[no_mangle]
pub extern fn Mix_FadeOutGroup(tag: i32, ms: i32) -> i32 {
  die("Mix_FadeOutGroup not implemented!");
  0
}
#[no_mangle]
pub extern fn Mix_HaltGroup(tag: i32) -> i32 {
  die("Mix_HaltGroup not implemented!");
  0
}

////
//// SFX functions ////
////

#[no_mangle]
pub extern fn Mix_RegisterEffect(channel: i32, f: *const u8, d: *const u8, arg: *const u8) -> i32 {
  die("Mix_RegisterEffect not implemented!");
  1
}
#[no_mangle]
pub extern fn Mix_UnregisterEffect(channel: i32, f: *const u8) -> i32 {
  die("Mix_UnregisterEffect not implemented!");
  1
}
#[no_mangle]
pub extern fn Mix_UnregisterAllEffects(channel: i32) -> i32 {
  die("Mix_UnregisterAllEffects not implemented!");
  1
}
#[no_mangle]
pub extern fn Mix_SetPostMix(f: *const u8, arg: *const u8) -> () {
  die("Mix_SetPostMix not implemented!");
}

#[no_mangle]
pub extern fn Mix_SetDistance(channel: i32, distance: u8) -> i32 {
  die("Mix_SetDistance not implemented!");
  1
}
#[no_mangle]
pub extern fn Mix_SetPosition(channel: i32, angle: i16, distance: u8) -> i32 {
  die("Mix_SetPosition not implemented!");
  1
}
#[no_mangle]
pub extern fn Mix_SetReverseStereo(channel: i32, flip: i32) -> i32 {
  die("Mix_SetReverseStereo not implemented!");
  1
}


//// What the hell does this do? ////
#[no_mangle]
pub extern fn Mix_SetSynchroValue(value: i32) -> i32 {
  die("Mix_SetSynchroValue not implemented!");
  0
}

