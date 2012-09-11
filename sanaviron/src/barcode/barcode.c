/*
 * barcode.c -- GNU barcode/ECC200 ISO/IEC16022/POSTNET interface for Python
 *
 * Copyright (c) 2009 Juan Manuel Mouriz (jmouriz@gmail.com)
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 * http://www.onefour.net/barcode/
 */
//#include <dlfcn.h>
//#define module void *
//#define open_library(library) dlopen(library, RTLD_LAZY)
//#define load_symbol dlsym
//#define close_library dlclose

#include <windows.h>
#define module HMODULE
#define open_library LoadLibrary
#define load_symbol GetProcAddress
#define close_library FreeLibrary

#include "barcode.h"

char *
get_code_data (int type, char *code, double width, double height)
{
   module library;

   if (type < POSTNET)
      library = open_library ("../src/barcode/lineal.so");
   else if (type < DATAMATRIX)
      library = open_library ("postnet/postnet.so");
   else if (type == DATAMATRIX)
      library = open_library ("datamatrix/datamatrix.so");
   else
      return NULL; /* TODO: report error */

   if (!library)
      return NULL; /* TODO: report error */

   void *symbol = load_symbol (library, "get_code_data");

   if (!symbol)
   {
      close_library (library);
      return NULL; /* TODO: report error */
   }

   typedef char *(*function) (int, char *, double, double);
   function handler = (function) symbol;

   char *buffer = (char *) malloc (4096);
   buffer = handler (type, code, width, height);
   close_library (library);

   return buffer;
}

char *
get_text_data (int type, char *code)
{
   if (type > BARCODE_93) return NULL;

   module library = open_library ("lineal/lineal.so");

   if (!library)
      return NULL; /* TODO: report error */

   void *symbol = load_symbol (library, "get_text_data");

   if (!symbol)
   {
      close_library (library);
      return NULL; /* TODO: report error */
   }

   typedef char *(*function) (int, char *);
   function handler = (function) symbol;

   char *buffer = (char *) malloc (4096);
   buffer = handler (type, code);
   close_library (library);

   return buffer;
}
