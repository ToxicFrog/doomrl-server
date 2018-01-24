# Use `make` for linux version, `mingw32-make windows` for windows.

CFLAGS=-g -Wall -Werror -std=gnu99 -shared -fPIC
MINGW_LIBS=-L/usr/i686-w64-mingw32/sys-root/mingw/lib/

all: linux
linux: libSDL_mixer-1.2.so.0
windows: SDL_mixer.dll

SDL_mixer.dll: libttysound.c stubs.c
	$(CC) $(MINGW_LIBS) $(CFLAGS) -o $@ $+ -lSDL

libSDL_mixer-1.2.so.0: libttysound.c stubs.c
	$(CC) $(CFLAGS) -o $@ $+

clean:
	rm -f libSDL_mixer-1.2.so.0 SDL_mixer.dll
