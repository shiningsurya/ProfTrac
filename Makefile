pt: ./pt.c
	gcc pt.c -fPIC -o $@ -lgsl -lm -lcblas -shared

clean:
	-rm -rf pt ptse ptpse
ptse: ./ptScaleEnergy.c
	gcc ./ptScaleEnergy.c -fPIC -o $@ -lgsl -lm -lcblas -shared
ptpse: ./ptScalePerEnergy.c
	gcc ./ptScalePerEnergy.c -fPIC -o $@ -lgsl -lm -lcblas -shared

.PHONY: clean
