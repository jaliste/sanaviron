CC = gcc
#CC = i586-mingw32msvc-gcc
CFLAGS = -g -O2 -Wall -DHAVE_UNISTD_H=1 -DHAVE_STRCASECMP=1 -DNO_LIBPAPER -fPIC
TARGET = lineal
SHARED = $(TARGET).so
#SHARED = $(TARGET).dll
HEADER = $(TARGET).h

INSTALL = /usr/bin/install -c

LDFLAGS = -L. -l$(TARGET) 

DSTDIR = ../../../objects/barcode

LIBOBJECTS = \
   interface.o \
   library.o \
   ean.o \
   code128.o \
   code39.o \
   code93.o \
   i25.o \
   msi.o \
   plessey.o \
   codabar.o \
   ps.o \
   pcl.o

ALLSOURCES = $(LIBOBJECTS:.o=.c)

RM = rm

all: $(SHARED)

$(SHARED): $(LIBOBJECTS)
	$(CC) -shared -o $(SHARED) $(LIBOBJECTS)

install:
	$(INSTALL) -c -m 0644 $(SHARED) $(DSTDIR) 

uninstall:
	$(RM) -f $(DSTDIR)/$(SHARED)

# Make clean keeps the compiled documents
clean:
	-$(RM) -f *.o */*.o *~ */*~ core test test.exe

# Make purge remove the compiled documents
purge: clean
	-$(RM) -f */*.o *~ */*~ core $(SHARED)

test: test.c $(SHARED)
	gcc $^ -o $@
