#![allow(non_snake_case)]
#![allow(unused_variables)]
#![allow(non_camel_case_types)]
#![allow(unreachable_code)]

extern crate libc;

use libc::exit;
use std::ffi::CString;
use std::io::stderr;
use std::io::Write;
use std::mem;
use std::str;
use std::ptr;

fn die(msg: &str) {
  writeln!(&mut stderr(), "FATAL: {}", msg)
    .ok().expect("Error writing error message :(");
  unsafe { exit(1) }
}

#[repr(C)]
pub struct SDL_Version {
  major: u8,
  minor: u8,
  patch: u8,
}

//// SDL_RWops ////

#[repr(C)]
pub struct SDL_RWops {
  seek: extern "C" fn(src: *mut SDL_RWops, offset: i32, whence: i32) -> i32,
  read: extern "C" fn(src: *mut SDL_RWops, dst: *mut u8, size: i32, count: i32) -> i32,
  write: *const libc::c_void,
  close: extern "C" fn(src: *mut SDL_RWops) -> i32,
  // a bunch of other stuff we don't care about
}

unsafe fn SDL_RWseek(src: *mut SDL_RWops, offset: i32, whence: i32) -> i32 {
  ((*src).seek)(src, offset, whence)
}

unsafe fn SDL_RWread(src: *mut SDL_RWops, dst: *mut u8, size: i32, count: i32) -> i32 {
  ((*src).read)(src, dst, size, count)
}

unsafe fn SDL_RWclose(src: *mut SDL_RWops) -> i32 {
  ((*src).close)(src)
}

//// General functions ////

static SDL_MIXER_VERSION: SDL_Version = SDL_Version { major: 1, minor: 2, patch: 10 };

#[no_mangle]
pub unsafe extern fn Mix_Linked_Version() -> *const SDL_Version {
  &SDL_MIXER_VERSION as *const SDL_Version
}

#[no_mangle]
pub extern fn Mix_OpenAudio(frequency: i32, format: u16, channels: i32, chunksize: i32) -> i32 {
  // unsafe {
  //   let ver = SDL_Linked_Version();
  //   println!("SDL initialized, version={}.{}.{}", (*ver).major, (*ver).minor, (*ver).patch);
  // }
  0
}
#[no_mangle]
pub extern fn Mix_CloseAudio() -> () {}

#[no_mangle]
pub unsafe extern fn Mix_QuerySpec(frequency: *mut i32, format: *mut u16, channels: *mut i32) -> i32 {
  *frequency = 22050;
  *format = 0x8010;
  *channels = 8;
  1
}

// unused: Mix_Init, Mix_Quit, Mix_CloseAudio, Mix_SetError
// implemented in Pascal: Mix_GetError

////
//// Sampling functions ////
////

fn report(delay: u32, row: u8, msg: String) -> () {
  print!("\x1B[{};1H\x1B[1m{}", row, msg);
  std::io::stdout().flush();
  std::thread::sleep_ms(delay);
  print!("\x1B[{};1H\x1B[0m{}", row, msg);
  std::io::stdout().flush();
}

#[repr(C)]
pub struct Mix_Chunk;

#[no_mangle]
pub unsafe extern fn Mix_LoadWAV_RW(src: *mut SDL_RWops, freesrc: i32) -> *const libc::c_void {
  let size = SDL_RWseek(src, 0, 2); // SEEK_END
  SDL_RWseek(src, 0, 0); // SEEK_SET; rewind
  let mut buf: Box<Vec<u8>> = Box::new(vec![0; size as usize]);
  report(500, 30, format!("LoadWAV: read={}", SDL_RWread(src, (*buf).as_mut_ptr(), 1, size)));
  {
    let desc = String::from_utf8_lossy(&*buf);
    report(500, 31, format!("LoadWAV: size={}, bytes={:?}", size, buf));
    report(500, 32, format!("LoadWAV: '{}'", desc.trim()));
  }
  if freesrc != 0 {
    SDL_RWclose(src);
  }
  mem::transmute(buf)
}
#[no_mangle]
pub extern fn Mix_QuickLoad_WAV(mem: *const u8) -> *const Mix_Chunk {
  die("Mix_QuickLoad_WAV not implemented.");
  ptr::null()
}
#[no_mangle]
pub extern fn Mix_VolumeChunk(chunk: *const Mix_Chunk, volume: i32) -> i32 {
  die("Mix_VolumeChunk not implemented.");
  volume
}

#[no_mangle]
pub unsafe extern fn Mix_FreeChunk(chunk: *const Mix_Chunk) -> () {
  let buf: Box<Vec<u8>> = mem::transmute_copy(&chunk); // freed when it leaves scope
}

////
//// Channel functions ////
////

#[no_mangle]
pub extern fn Mix_AllocateChannels(channels: i32) -> i32 {
  die("Mix_AllocateChannels not implemented!");
  channels
}

// TODO: remember what volume each channel has and take that into account so that
// the CC can display volume as well as sound.
#[no_mangle]
pub extern fn Mix_Volume(channel: i32, volume: i32) -> i32 {
  report(500, 29, format!("Volume: {} at {}", channel, volume));
  volume
}

// It calls PlayChannelTimed, then volume, then panning

#[no_mangle]
pub unsafe extern fn Mix_PlayChannelTimed(channel: i32,
                                   chunk: *const libc::c_void,
                                   loops: i32,
                                   ticks: i32) -> i32 {
  report(500, 27, format!("Mix_PlayChannelTimed: c={} l={} t={}", channel, loops, ticks));
  let buf: Box<Vec<u8>> = mem::transmute_copy(&chunk); // Acquires ownership of chunk.
  {
    let desc = String::from_utf8_lossy(&*buf);
    report(500, 26, format!("You hear: {}", desc.trim()));
  }
  let buf: *const libc::c_void = mem::transmute(buf); // Relinquish ownership of chunk.
  0
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

// TODO: use these functions, if DoomRL employs them, to determine directionality
// of sound, e.g. "you hear <> to the west".
#[no_mangle]
pub extern fn Mix_SetPanning(channel: i32, left: u8, right: u8) -> i32 {
  report(500, 28, format!("Panning: {} L {} R {}", channel, left, right));
  1
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

//// Stuff implenented in Pascal using the above functions ////
// function Mix_LoadWAV( filename : PChar ) : PMix_Chunk;
// function Mix_PlayChannel( channel : integer; chunk : PMix_Chunk; loops : integer ) : integer;
// function Mix_FadeInChannel( channel : integer; chunk : PMix_Chunk; loops : integer; ms : integer ) : integer;
// function Mix_GetError : PChar;
// function Mix_LoadWAV( filename : PChar ) : PMix_Chunk;
// function Mix_PlayChannel( channel : integer; chunk : PMix_Chunk; loops : integer ) : integer;
// function Mix_FadeInChannel( channel : integer; chunk : PMix_Chunk; loops :
