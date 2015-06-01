////
//// SDL types used by the ttysound library.
////

extern crate libc;

#[repr(C)]
pub struct SDL_Version {
  pub major: u8,
  pub minor: u8,
  pub patch: u8,
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

pub unsafe fn SDL_RWseek(src: *mut SDL_RWops, offset: i32, whence: i32) -> i32 {
  ((*src).seek)(src, offset, whence)
}

pub unsafe fn SDL_RWread(src: *mut SDL_RWops, dst: *mut u8, size: i32, count: i32) -> i32 {
  ((*src).read)(src, dst, size, count)
}

pub unsafe fn SDL_RWclose(src: *mut SDL_RWops) -> i32 {
  ((*src).close)(src)
}

#[repr(C)]
pub struct Mix_Chunk;

