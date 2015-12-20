#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <time.h>
#include <string.h>

#include <SDL/SDL.h>
#include <SDL/SDL_version.h>
#include <SDL/SDL_rwops.h>

//// TTY display functions ////

// Display a message on the given row.
void emit_tty(uint8_t row, const char * msg) {
  printf("\x1B[%d;1H\x1B[2K\x1B[0m%s", row, msg);
  fflush(stdout);
}

// Display a bold message on the given row for delay ms, then replace it with
// a plain one.
void report_tty(uint32_t delay, uint8_t row, const char * msg) {
  printf("\x1B[%d;1H\x1B[2K\x1B[1m%s", row, msg);
  fflush(stdout);
  usleep(delay * 1000);
  emit_tty(row, msg);
}

//// SDL display functions ////

void emit_sdl(uint8_t unused_row, const char * msg) {
  char * caption; char * icon;
  SDL_WM_GetCaption(&caption, &icon);
  SDL_WM_SetCaption(msg, icon);
}

void report_sdl(uint32_t unused_delay, uint8_t unused_row, const char * msg) {
  emit_sdl(0, msg);
}

//// Function pointers ////

void (*emit)(uint8_t, const char *);
void (*report)(uint32_t, uint8_t, const char *);
const char * SEPARATOR;
const char * HEADER;

//// State ////

typedef struct SoundEvent {
  const char * sound;
  uint8_t panning;
  uint8_t volume;
  uint64_t turn;
  struct SoundEvent * prev;
} SoundEvent;

struct State {
  SoundEvent * last;
  double then;
  uint64_t turn;
  char * last_frame;
} state;

//// General functions ////

static SDL_version SDL_MIXER_VERSION = { 1, 2, 10 };

const SDL_version * Mix_Linked_Version() {
  return &SDL_MIXER_VERSION;
}

int32_t Mix_OpenAudio(int32_t freq, uint16_t format, int32_t channels, int32_t chunksize) {
  state.last = NULL;
  state.then = 0.0;
  state.turn = 0;
  state.last_frame = calloc(1, 1); // we can't just point it at a string constant because it gets free()d later

  if (SDL_GetVideoSurface()) {
    // We're in graphical mode.
    emit = emit_sdl;
    report = report_sdl;
    SEPARATOR = " | ";
    HEADER = "You hear:";
    report(500, 26, "You hear:  silence");
  } else {
    emit = emit_tty;
    report = report_tty;
    SEPARATOR = "\x1B[1;37m|\x1B[0m";
    HEADER = "  You hear:";
    report(500, 26, "  You hear:  silence");
  }

  return 0;
}
void Mix_CloseAudio() {}

int32_t Mix_QuerySpec(int32_t * freq, uint16_t * format, int32_t * channels) {
  *freq = 22050;
  *format = 0x8010;
  *channels = 8;
  return 1;
}

int32_t Mix_VolumeMusic(int32_t volume) {
  return volume;
}

// Unused: Mix_Init, Mix_Quit, Mix_CloseAudio, Mix_SetError
// Implemented in DoomRL: Mix_GetError

const char * Mix_LoadWAV_RW(SDL_RWops * src, int32_t freesrc) {
  SDL_RWseek(src, 0, RW_SEEK_END);
  uint32_t size = SDL_RWtell(src);
  SDL_RWseek(src, 0, RW_SEEK_SET);
  char * buf = malloc(size+1);
  SDL_RWread(src, (uint8_t *)buf, size, 1);
  buf[size] = '\0';

  if (freesrc) {
    SDL_RWclose(src);
  }

  return buf; // Caller takes ownership.
}

void Mix_FreeChunk(char * chunk) {
  free(chunk); // Caller relinquished ownership.
}

// It calls PlayChannelTimed, then volume, then panning

// No support for volume or panning yet. DoomRL does this kind of awkwardly by
// calling PlayChannelTimed first, and *then* calling Volume and SetPanning to
// set distance and direction. I don't know if it's guaranteed that Volume and
// SetPanning are called at all.

// TODO: remember what volume each channel has and take that into account so that
// the CC can display volume as well as sound.
int32_t Mix_Volume(int32_t channel, int32_t volume) {
  //report(10, 29, format!("Volume: {} at {}", channel, volume));
  return volume;
}

// TODO: directionality of sound.
int32_t Mix_SetPanning(int32_t channel, uint8_t left, uint8_t right) {
  //report(10, 28, format!("Panning: {} L {} R {}", channel, left, right));
  return 1;
}

uint8_t eventIsOld(const void * arg, SoundEvent * evt) {
  return state.turn - evt->turn >= 3;
}

uint8_t eventIsEqual(const void * arg, SoundEvent * evt) {
  // direct pointer comparison because two identical sounds will
  // be the same underlying string.
  return arg == evt->sound;
}

void deleteEventsIf(uint8_t (*pred)(const void *, SoundEvent *), const void * arg) {
  // Pointer to the pointer to the event we're investigating. This needs to be
  // updated if we delete the event.
  SoundEvent ** prevptr = &state.last;
  SoundEvent * evt = state.last;
  while (evt) {
    if (pred(arg, evt)) {
      *prevptr = evt->prev;
      free(evt);
      evt = *prevptr;
    } else {
      prevptr = &evt->prev;
    }
    evt = *prevptr;
  }
}

// Clear all events that are duplicates of this one, then push this event.
void pushEvent(const char * sound) {
  deleteEventsIf(eventIsEqual, sound);
  SoundEvent * evt = malloc(sizeof(SoundEvent));
  evt->sound = sound;
  evt->turn = state.turn;
  evt->panning = evt->volume = 0;
  evt->prev = state.last;
  state.last = evt;
}

int32_t Mix_PlayChannelTimed(int32_t channel, const char * chunk, int32_t loops, int32_t ticks) {
  struct timespec now_ts;
  clock_gettime(CLOCK_MONOTONIC, &now_ts);
  double now = (double)now_ts.tv_sec + ((double)now_ts.tv_nsec / 1000000000.0);
  double diff = now - state.then;

  if (diff >= 0.1) {
    state.turn++;
    deleteEventsIf(eventIsOld, NULL);
    // push soundevent containing | separator
    pushEvent(SEPARATOR);
  }

  if (strlen(chunk)) {
    pushEvent(chunk);
  }

  SoundEvent * evt = state.last;
  char * heard = calloc(12, 1);
  strcpy(heard, HEADER);
  while (evt) {
    // +1 for null terminator, +1 for separating space
    heard = realloc(heard, strlen(heard) + strlen(evt->sound) + 2);
    strcat(heard, " ");
    strcat(heard, evt->sound);
    evt = evt->prev;
  }

  if (strcmp(heard, state.last_frame)) {
    emit(26, heard);
    free(state.last_frame);
    state.last_frame = heard;
  } else {
    free(heard);
  }

  state.then = now;
  return 0;
}

