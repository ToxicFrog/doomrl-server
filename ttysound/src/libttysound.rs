#![allow(non_snake_case)]
#![allow(unused_variables)]
#![allow(non_camel_case_types)]
#![allow(unreachable_code)]

#[macro_use]
extern crate lazy_static;

extern crate libc;
extern crate time;

use std::collections::HashSet;

use std::io::Write;
use std::mem;

mod types;
use types::*;

pub mod stubs;

fn report(delay: u32, row: u8, msg: String) -> () {
  print!("\x1B[{};1H\x1B[2K\x1B[1m{}", row, msg);
  std::io::stdout().flush();
  std::thread::sleep_ms(delay);
  print!("\x1B[{};1H\x1B[0m{}", row, msg);
  std::io::stdout().flush();
}

//// General functions ////

static SDL_MIXER_VERSION: SDL_Version = SDL_Version { major: 1, minor: 2, patch: 10 };

#[no_mangle]
pub unsafe extern fn Mix_Linked_Version() -> *const SDL_Version {
  &SDL_MIXER_VERSION as *const SDL_Version
}

#[no_mangle]
pub extern fn Mix_OpenAudio(frequency: i32, format: u16, channels: i32, chunksize: i32) -> i32 {
  report(500, 26, format!("Sounds: initialized"));
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

#[no_mangle]
pub unsafe extern fn Mix_LoadWAV_RW(src: *mut SDL_RWops, freesrc: i32) -> *const libc::c_void {
  let size = SDL_RWseek(src, 0, 2); // SEEK_END
  SDL_RWseek(src, 0, 0); // SEEK_SET; rewind
  let mut buf: Box<Vec<u8>> = Box::new(vec![0; size as usize]);
  SDL_RWread(src, (*buf).as_mut_ptr(), 1, size);
  // {
  //   let desc = String::from_utf8_lossy(&*buf);
  //   report(50, 26, format!("Sounds: '{}'", desc.trim()));
  // }
  if freesrc != 0 {
    SDL_RWclose(src);
  }
  mem::transmute(buf)
}

#[no_mangle]
pub unsafe extern fn Mix_FreeChunk(chunk: *const Mix_Chunk) -> () {
  let buf: Box<Vec<u8>> = mem::transmute_copy(&chunk); // freed when it leaves scope
}

////
//// Channel functions ////
////

// TODO: remember what volume each channel has and take that into account so that
// the CC can display volume as well as sound.
#[no_mangle]
pub extern fn Mix_Volume(channel: i32, volume: i32) -> i32 {
  //report(10, 29, format!("Volume: {} at {}", channel, volume));
  volume
}

// TODO: use these functions, if DoomRL employs them, to determine directionality
// of sound, e.g. "you hear <> to the west".
#[no_mangle]
pub extern fn Mix_SetPanning(channel: i32, left: u8, right: u8) -> i32 {
  //report(10, 28, format!("Panning: {} L {} R {}", channel, left, right));
  1
}

// It calls PlayChannelTimed, then volume, then panning

lazy_static! {
  static ref SOUNDQ: std::sync::Mutex<HashSet<String>> = std::sync::Mutex::new(HashSet::new());
}
static mut sound_time: u64 = 0;

#[no_mangle]
pub unsafe extern fn Mix_PlayChannelTimed(channel: i32,
                                   chunk: *const libc::c_void,
                                   loops: i32,
                                   ticks: i32) -> i32 {
  let now = time::precise_time_ns();
  if (now - sound_time) > 100*1000*1000 { // 100ms
    // report and clear time
    let mut soundq = SOUNDQ.lock().unwrap();
    (*soundq).clear();
    //report(10, 27, format!("Clear queue, st={}, now={}", sound_time/1000/1000, now/1000/1000));
  }
  let buf: Box<Vec<u8>> = mem::transmute_copy(&chunk); // Acquires ownership of chunk.
  {
    let desc = String::from_utf8_lossy(&*buf);
    let mut soundq = SOUNDQ.lock().unwrap();
    (*soundq).insert(desc.trim().to_string());
    report(33, 26, format!("  You hear:{}", (*soundq).iter().fold("".to_string(), |l,r| { l + "  " + &r })));
    //soundq.push_front(desc.clone());
    //report(10, 26, format!("  You hear: {}", desc.trim()));
  }
  //report(10, 27, format!("Mix_PlayChannelTimed: c={} l={} t={}", channel, loops, ticks));
  sound_time = time::precise_time_ns();
  let buf: *const libc::c_void = mem::transmute(buf); // Relinquish ownership of chunk.
  0
}
