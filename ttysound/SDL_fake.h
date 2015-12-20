// Implementation of some simple SDL types and functions we need.
// This way users don't need libSDL-devel installed.

#include <stdint.h>

typedef struct SDL_version {
  uint8_t major;
  uint8_t minor;
  uint8_t patch;
} SDL_version;

typedef struct SDL_RWops {
  int32_t (*seek)(struct SDL_RWops *, int32_t, int32_t);
  int32_t (*read)(struct SDL_RWops *, uint8_t *, int32_t, int32_t);
  void * write; // Don't care about this fn
  int32_t (*close)(struct SDL_RWops *);
  // Or about any of the other struct members, and since we're only ever passing
  // these by pointer, we don't need to.
} SDL_RWops;

enum {
  RW_SEEK_SET = 0,
  RW_SEEK_CUR = 1,
  RW_SEEK_END = 2,
} SDL_RWseek;

#define   SDL_RWseek(ctx, offset, whence)   (ctx)->seek(ctx, offset, whence)
#define   SDL_RWtell(ctx)   (ctx)->seek(ctx, 0, RW_SEEK_CUR)
#define   SDL_RWread(ctx, ptr, size, n)   (ctx)->read(ctx, ptr, size, n)
#define   SDL_RWclose(ctx)   (ctx)->close(ctx)
