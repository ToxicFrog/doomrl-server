#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <time.h>
#include <string.h>

#include <SDL/SDL.h>
#include <SDL/SDL_version.h>
#include <SDL/SDL_rwops.h>

#define max(x, y) ((x > y) ? x : y)

//// TTY display functions ////

// Extremely quick and dirty function to calculate the display width, on a vt220,
// of a cstring. Assumes that the only control sequences are CSI ... m and that
// all ESC characters start a CSI.
size_t vt220len(const char * str) {
  size_t len = 0;
  uint8_t nonprinting = 0;
  for (size_t i = 0; str[i]; ++i) {
    unsigned char c  = str[i];
    if (c == '\x1B') {
      nonprinting = 1;
    } else if (nonprinting && c == 'm') {
      nonprinting = 0;
    } else if (!nonprinting) {
      ++len;
    }
  }
  return len;
}

// Display a message on the given row, centered.
void emit_tty(uint8_t row, int col, const char * msg) {
  printf("\x1B[%d;1H\x1B[2K\x1B[0m%*s%s", row, col, "", msg);
  fflush(stdout);
}

//// SDL display functions ////

void emit_sdl(uint8_t unused_row, int col, const char * msg) {
  char * caption; char * icon;
  SDL_WM_GetCaption(&caption, &icon);
  SDL_WM_SetCaption(msg, icon);
}

//// Function pointers ////

void (*emit)(uint8_t, int, const char *);
const char * LSEP;
const char * RSEP;
const char * HEADER;

//// State ////

typedef struct SoundEvent {
  const char * sound;
  uint8_t panning;
  uint8_t volume;
  uint64_t turn;
  struct SoundEvent * next;
} SoundEvent;

struct State {
  SoundEvent * last;
  SoundEvent * left;
  SoundEvent * center;
  SoundEvent * right;
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
  state.left = state.center = state.right = state.last = NULL;
  state.then = 0.0;
  state.turn = 0;
  state.last_frame = calloc(1, 1); // we can't just point it at a string constant because it gets free()d later

  if (SDL_GetVideoSurface()) {
    // We're in graphical mode.
    emit = emit_sdl;
    LSEP = " ((";
    RSEP = " ))";
    emit(26, 36, "(( @ ))");
  } else {
    emit = emit_tty;
    LSEP = " \x1B[1;37m((\x1B[0m";
    RSEP = " \x1B[1;37m))\x1B[0m";
    emit(26, 36, "\x1B[1m(( @ ))");
    usleep(500 * 1000);
    emit(26, 36, "(( @ ))");
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

//// Internal functions for actually recording and displaying sound events. ////

uint8_t constantlyTrue(const void * arg, SoundEvent * evt) {
  return 1;
}

uint8_t eventIsEqual(const void * arg, SoundEvent * evt) {
  // direct pointer comparison because two identical sounds will
  // be the same underlying string.
  return arg == evt->sound;
}

void deleteEventsIf(SoundEvent ** head,
                    uint8_t (*pred)(const void *, SoundEvent *),
                    const void * arg) {
  SoundEvent * evt = *head;
  while (evt) {
    if (pred(arg, evt)) {
      *head = evt->next;
      free(evt);
    } else {
      head = &evt->next;
    }
    evt = *head;
  }
}

void clearEvents() {
  deleteEventsIf(&state.left, constantlyTrue, NULL);
  deleteEventsIf(&state.center, constantlyTrue, NULL);
  deleteEventsIf(&state.right, constantlyTrue, NULL);
}

// Install this event in the corresponding list.
// If a duplicate of this event exists, but is louder, delete this event and return.
// If a duplicate of this event exists, but is quieter, delete *that* event.
// Then, insert the event into the list such that it is sorted by volume descending.
void pushEvent(SoundEvent ** head, SoundEvent * new) {
  new->next = *head;
  *head = new;
  return;

}

// Given a chain of SoundEvents, calculate the total size, in bytes, + sepsize
// bytes per event for a separator.
size_t soundLength(SoundEvent * head, size_t sepsize) {
  size_t len = 0;
  while (head) {
    len += strlen(head->sound) + sepsize;
    head = head->next;
  }
  return len;
}

void soundcat(char * str, SoundEvent * evt) {
  while (evt) {
    strcat(str, " ");
    strcat(str, evt->sound);
    evt = evt->next;
  }
}

void displaySounds() {
  size_t bytes = strlen(LSEP) + strlen(RSEP)
               + soundLength(state.left, 1)
               + soundLength(state.center, 1)
               + soundLength(state.right, 1)
               + 1; // null terminator
  char * heard = calloc(bytes, 1);

  soundcat(heard, state.left);
  size_t leftlen = vt220len(heard);

  strcat(heard, LSEP);
  soundcat(heard, state.center);
  strcat(heard, RSEP);

  size_t centerlen = vt220len(heard) - leftlen;

  soundcat(heard, state.right);

  if (strcmp(heard, state.last_frame)) {
    emit(26, max(0, (80-centerlen)/2), heard);
    free(state.last_frame);
    state.last_frame = heard;
  } else {
    free(heard);
  }
}

//// SDL functions called by DoomRL to play sounds. ////

// DoomRL calls Mix_PlayChannelTimed *first*, then calls Mix_Volume and
// Mix_SetPanning immediately afterwards. It always calls all three of them
// and always in this order, so we push the event when Mix_PlayChannelTimed is
// called, then fill in volume and panning information afterwards, and display
// the event after filling in panning information.

// Volume is always between 0 (completely silent) and 128 (MIX_MAX_VOLUME). In
// practice DoomRL never seems to go above 99.
int32_t Mix_Volume(int32_t channel, int32_t volume) {
  if (!state.last) return volume;

  //fprintf(stderr, "volume: %d %d\n", channel, volume);
  state.last->volume = volume;
  return volume;
}

// left + right == 255, always
// so, panning 255: all left, 0: all right, 127: directly north/south of the player
int32_t Mix_SetPanning(int32_t channel, uint8_t left, uint8_t right) {
  if (!state.last) return 1;
  //fprintf(stderr, "panning: %d %d %d\n", channel, left, right);
  state.last->panning = 255 - right;

  // Move event to the correct list.
  SoundEvent ** headptr = &state.center;
  if (state.last->panning >= 144) {
    headptr = &state.left;
  } else if (state.last->panning <= 112) {
    headptr = &state.right;
  }
  pushEvent(headptr, state.last);
  state.last = NULL;

  // SetPanning is always called last for each sound effect, so at this point we
  // have all the information we need and can display it.
  displaySounds();

  return 1;
}

int32_t Mix_PlayChannelTimed(int32_t channel, const char * chunk, int32_t loops, int32_t ticks) {
  //fprintf(stderr, "PlayChannel %d %s\n", channel, chunk);
  struct timespec now_ts;
  clock_gettime(CLOCK_MONOTONIC, &now_ts);
  double now = (double)now_ts.tv_sec + ((double)now_ts.tv_nsec / 1000000000.0);
  double diff = now - state.then;

  if (diff >= 0.1) {
    clearEvents();
    state.turn++;
  }

  if (strlen(chunk)) {
    SoundEvent * evt = malloc(sizeof(SoundEvent));
    evt->sound = chunk;
    evt->turn = state.turn;
    evt->panning = evt->volume = 0;
    evt->next = NULL;
    state.last = evt;
  }

  state.then = now;
  return 0;
}
