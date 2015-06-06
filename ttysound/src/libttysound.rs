#![allow(non_snake_case)]
#![allow(unused_variables)]
#![allow(non_camel_case_types)]
#![allow(unreachable_code)]

#[macro_use]
extern crate lazy_static;

extern crate libc;
extern crate time;

use std::collections::HashSet;
use std::collections::VecDeque;

use std::io::Write;
use std::mem;

mod types;
use types::*;

pub mod stubs;

fn emit(row: u8, msg: String) -> () {
  print!("\x1B[{};1H\x1B[2K\x1B[0m{}", row, msg);
  std::io::stdout().flush().unwrap();
}

fn report(delay: u32, row: u8, msg: String) -> () {
  print!("\x1B[{};1H\x1B[2K\x1B[1m{}", row, msg);
  std::io::stdout().flush().unwrap();
  std::thread::sleep_ms(delay);
  emit(row, msg);
}

//// General functions ////

static SDL_MIXER_VERSION: SDL_Version = SDL_Version { major: 1, minor: 2, patch: 10 };

#[no_mangle]
pub unsafe extern fn Mix_Linked_Version() -> *const SDL_Version {
  &SDL_MIXER_VERSION as *const SDL_Version
}

#[no_mangle]
pub extern fn Mix_OpenAudio(frequency: i32, format: u16, channels: i32, chunksize: i32) -> i32 {
  report(500, 26, format!("  You hear:  silence"));
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

struct SoundEvent {
  sound: String,
  panning: u8,
  volume: u8,
  turn: u64,
}
struct SoundState {
  sounds: VecDeque<SoundEvent>,
  time: u64,
  turn: u64,
  last_frame: String,
}
lazy_static! {
  static ref STATE: std::sync::Mutex<SoundState> = std::sync::Mutex::new(SoundState {
    sounds: VecDeque::new(),
    time: 0,
    turn: 0,
    last_frame: String::new(),
  });
}

#[no_mangle]
pub unsafe extern fn Mix_PlayChannelTimed(channel: i32,
                                   chunk: *const libc::c_void,
                                   loops: i32,
                                   ticks: i32) -> i32 {
  let now = time::precise_time_ns();
  //Get a &mut SoundState (from the Mutex), and then do `let SoundState { ref mut sounds, ref mut last_frame } = *sound_state_ref;`
  let mut state_guard = STATE.lock().unwrap();
  let SoundState { ref mut sounds, ref mut last_frame, ref mut time, ref mut turn } = *&mut *state_guard;
  if (now - *time) > 100*1000*1000 { // 100ms
    // report and clear time
    *turn += 1;
    loop {
      let remove = match sounds.back() {
        Some(evt) => (*turn - evt.turn) >= 3,
        None => break
      };
      if remove {
        sounds.pop_back();
      } else {
        break
      }
    }
    sounds.push_front(SoundEvent {
      sound: "\x1B[1;37m|\x1B[0m".to_string(),
      panning: 0,
      volume: 0,
      turn: *turn,
    })
  }
  let buf: Box<Vec<u8>> = mem::transmute_copy(&chunk); // Acquires ownership of chunk.
  {
    if buf.len() > 1 {
      let desc = String::from_utf8_lossy(&*buf);
      sounds.push_front(SoundEvent {
        sound: desc.trim().to_string(),
        panning: 0,
        volume: 0,
        turn: *turn,
      });
    }
    let mut seen: HashSet<&String> = HashSet::new();
    let heard: String = sounds.iter()
                              .filter(|evt| if seen.contains(&evt.sound) { false } else { seen.insert(&evt.sound); true })
                              .fold("".to_string(), |l,r| { l + "  " + &r.sound });
    if heard != *last_frame {
      emit(26, format!("  You hear:{}", heard));
      *last_frame = heard;
    }
  }
  let buf: *const libc::c_void = mem::transmute(buf); // Relinquish ownership of chunk.
  *time = time::precise_time_ns();
  0
}
