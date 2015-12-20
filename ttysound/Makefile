CFLAGS=-g -Wall -Werror -std=gnu99 -fPIC -shared

libttysound.so: libttysound.c stubs.c SDL_fake.h
	$(CC) $(CFLAGS) -o $@ $+

clean:
	rm -f libttysound.so
