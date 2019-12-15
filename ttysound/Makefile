# Use `make` for linux version, `mingw32-make windows` for windows.

CFLAGS=-g -Wall -Werror -std=gnu99 -shared -fPIC
MINGW_LIBS=-L/usr/i686-w64-mingw32/sys-root/mingw/lib/

SCRIPTS=$(wildcard doomrl_cc_*)
DATA=cc README.md config.lua

SO_NAME=libSDL_mixer-1.2.so.0
DLL_NAME=SDL_mixer.dll
ZIP_NAME=doomrl-closedcaptions-$(shell git describe --tags).zip

DRL_SOUND_CONFIG=soundhq.lua

all: linux ccfiles
linux: $(SO_NAME)
windows: $(DLL_NAME)
zip: $(ZIP_NAME)

$(ZIP_NAME): libwinpthread-1.dll $(DLL_NAME) $(SO_NAME) $(SCRIPTS) $(DATA)
	zip -r $@ $+

$(DLL_NAME): libttysound.c stubs.c
	$(CC) $(MINGW_LIBS) $(CFLAGS) -o $@ $+ -lSDL

$(SO_NAME): libttysound.c stubs.c
	$(CC) $(CFLAGS) -o $@ $+

ccfiles: $(DRL_SOUND_CONFIG)
	lua generate-cc-files.lua "$(DRL_SOUND_CONFIG)"

# FIXME: probably doesn't work on not-SUSE
libwinpthread-1.dll: /usr/i686-w64-mingw32/sys-root/mingw/bin/libwinpthread-1.dll
	cp $< $@

clean:
	rm -f *.zip $(DLL_NAME) $(SO_NAME)
