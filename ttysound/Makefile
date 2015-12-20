CFLAGS=-g -Wall -Werror -std=gnu99 -fPIC -shared -lSDL

libttysound.so: libttysound.c stubs.c
	$(CC) $(CFLAGS) -o $@ $+

clean:
	rm -f libttysound.so
