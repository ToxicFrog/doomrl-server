/*
 * Stubbed out functions. These are looked up by DoomRL using dlsym(), but
 * never actually called.
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

void die(const char * msg) {
  fprintf(stderr, "FATAL: %s\n", msg);
  exit(1);
}

#define STUB(name, rtype, ...) rtype name (__VA_ARGS__) { \
  die(#name " not implemented."); \
  return (rtype)0; \
}

/*
 * Sample functions
 */

STUB(Mix_QuickLoad_WAV, void *, const uint8_t * mem);
STUB(Mix_VolumeChunk, uint32_t, void * chunk, uint32_t volume);

/*
 * Channel functions
 */

STUB(Mix_AllocateChannels, uint32_t, uint32_t channels);
STUB(Mix_FadeInChannelTimed, uint32_t,
     uint32_t channel, void * chunk, uint32_t loops, uint32_t ms, uint32_t ticks);

STUB(Mix_Pause, void, uint32_t channel);
STUB(Mix_Resume, void, uint32_t channel);

STUB(Mix_HaltChannel, uint32_t, uint32_t channel);
STUB(Mix_ExpireChannel, uint32_t, uint32_t channel, uint32_t ticks);
STUB(Mix_FadeOutChannel, uint32_t, uint32_t channel, uint32_t ms);
STUB(Mix_ChannelFinished, void, uint8_t * f);

STUB(Mix_Paused, uint32_t, uint32_t channel);
STUB(Mix_Playing, uint32_t, uint32_t channel);
STUB(Mix_FadingChannel, uint32_t, uint32_t channel);
STUB(Mix_GetChunk, void *, uint32_t channel);

STUB(Mix_LoadMUS, void *, const char * file);
STUB(Mix_LoadMUS_RW, void *, const uint8_t * rw);

STUB(Mix_PlayMusic, uint32_t, void * music, uint32_t loops);
STUB(Mix_FadeInMusic, uint32_t, void * music, uint32_t loops, uint32_t ms);
STUB(Mix_FadeOutMusic, uint32_t, uint32_t ms);
STUB(Mix_HookMusic, void, void * f, void * arg);
STUB(Mix_HookMusicFinished, void, void * f);

STUB(Mix_PauseMusic, void);
STUB(Mix_ResumeMusic, void);
STUB(Mix_HaltMusic, void);
STUB(Mix_RewindMusic, void);
STUB(Mix_SetMusicPosition, uint32_t, double position);
STUB(Mix_SetMusicCMD, uint32_t, void * command);

STUB(Mix_GetMusicType, uint32_t, void * music);
STUB(Mix_PlayingMusic, uint32_t);
STUB(Mix_PausedMusic, uint32_t);
STUB(Mix_FadingMusic, uint32_t);
STUB(Mix_GetMusicHookData, void *);
STUB(Mix_FreeMusic, void, void * mus);

STUB(Mix_ReserveChannels, uint32_t, uint32_t num);
STUB(Mix_GroupChannel, uint32_t, uint32_t which, uint32_t tag);
STUB(Mix_GroupChannels, uint32_t, uint32_t from, uint32_t to, uint32_t tag);
STUB(Mix_GroupCount, uint32_t, uint32_t tag);
STUB(Mix_GroupAvailable, uint32_t, uint32_t tag);
STUB(Mix_GroupOldest, uint32_t, uint32_t tag);
STUB(Mix_GroupNewer, uint32_t, uint32_t tag);
STUB(Mix_FadeOutGroup, uint32_t, uint32_t tag, uint32_t ms);
STUB(Mix_HaltGroup, uint32_t, uint32_t tag);

STUB(Mix_RegisterEffect, uint32_t, uint32_t channel, void * f, void * d, void * arg);
STUB(Mix_UnregisterEffect, uint32_t, uint32_t channel, void * f);
STUB(Mix_UnregisterAllEffects, uint32_t, uint32_t channel);
STUB(Mix_SetPostMix, void, void * f, void * arg);

STUB(Mix_SetDistance, uint32_t, uint32_t channel, uint8_t distance);
STUB(Mix_SetPosition, uint32_t, uint32_t channel, uint16_t angle, uint8_t distance);
STUB(Mix_SetReverseStereo, uint32_t, uint32_t channel, uint32_t flip);

STUB(Mix_SetSynchroValue, uint32_t, uint32_t value);
