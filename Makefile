pt:
	gcc pt.c -fPIC -o $@ -lgsl -lm -lcblas -shared

clean:
	-rm -rf pt

