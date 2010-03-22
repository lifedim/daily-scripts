PYINC = /System/Library/Frameworks/Python.framework/Headers 
MODULE = lookup

_$(MODULE).so : $(MODULE)_wrap.c lib$(MODULE).so
	gcc -shared -I$(PYINC) -framework Python -L. -l$(MODULE) -o _$(MODULE).so $(MODULE)_wrap.c

lib$(MODULE).so : $(MODULE).c
	gcc -shared -lz -o lib$(MODULE).so $(MODULE).c

$(MODULE)_wrap.c $(MODULE).py : $(MODULE).i
	swig -python $(MODULE).i

clean:
	rm -f $(MODULE)_wrap.c $(MODULE).py lib$(MODULE).so _$(MODULE).so

