# This Makefile should run fine with both pmake and gmake

CC = gcc
#CC = i586-mingw32msvc-gcc
CFLAGS = -g -O2 -Wall -DHAVE_UNISTD_H=1 -DHAVE_STRCASECMP=1 -DNO_LIBPAPER -fPIC
#RANLIB = ranlib
TARGET = barcode
SHARED = $(TARGET).so
#SHARED = $(TARGET).dll
HEADER = $(TARGET).h

INSTALL = /usr/bin/install -c

LDFLAGS = -L. -l$(TARGET) 

prefix = /usr/local
BINDIR = $(prefix)/bin
LIBDIR = $(prefix)/lib
INCDIR = $(prefix)/include

LIBOBJECTS = \
   barcode.o \
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

#Hmm... "RM" is undefined in pmake
RM = rm

all: $(SHARED)

$(SHARED): $(LIBOBJECTS)
	$(CC) -shared -o $(SHARED) $(LIBOBJECTS)
	#$(AR) r $(SHARED) $(LIBOBJECTS)
	#$(RANLIB) $(SHARED)

install:
	$(INSTALL) -d $(INCDIR) $(LIBDIR)
	$(INSTALL) -c -m 0644 $(HEADER) $(INCDIR)
	$(INSTALL) -c -m 0644  $(SHARED) $(LIBDIR)

uninstall:
	$(RM) -f $(INCDIR)/$(HEADER)
	$(RM) -f $(LIBDIR)/$(SHARED)

# Make clean keeps the compiled documents
clean:
	-$(RM) -f *.o */*.o *~ */*~ core

# Make purge remove the compiled documents
purge: clean
	-$(RM) -f */*.o *~ */*~ core $(SHARED)
