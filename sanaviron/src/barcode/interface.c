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
 */
#include <stdlib.h>
#include <string.h>

#include "interface.h"

#define MIN_PIXEL_SIZE 1.0

char *
barcode_get_code_data (int type, char *code, double width, double height)
{
  int oflags = type | BARCODE_OUT_PS | BARCODE_OUT_NOHEADERS;
  struct Barcode_Item *Bar = Barcode_Create (code);

  Barcode_Encode (Bar, oflags);

  if (Bar->error) return NULL;

  /* from:int svg_bars(struct Barcode_Item *bc, FILE *f) */
  char *partial = strdup (Bar->partial);
  int count = strlen (partial);
  int i = 0; /* Loop counter */
  int x = 0; /* Where the current box is drawn on x */
  int y = 0; /* Where the current box is drawn on y */
  int bar = 0;
  int size = 0;
  double ratio;
  double lenght;
  char *data;
  char *output;

  output = (char *) malloc (2048);
  
  while (i < count)
  {
    char current = *(partial + i) - 48;

    if (current > 9)
    {
      if (i + 1 >= count) break;
       
      current = *(partial + i + 1) - 48;
      i += 2;
    }
    
    x += current;
    i++;
  }
  
  ratio = width / x;
  i = 0;
  x = 0;
  
  while (i < count)
  {
    char current = *(partial + i) - 48;
  
    lenght = height; /* Guide bar */

    if (current > 9)
    {
      if (i + 1 >= count) break;
       
      current = *(partial + i + 1) - 48;
      i += 2;
    }
    else
      lenght -= 20;
    
    if (bar)
    {
      sprintf (output + size, "%d.0:%d.0:%.02f:%.02f ", x, y, current * ratio, lenght);
      size = strlen (output);
      /*
      fprintf (stdout, "cairo_move_to(context, %d, %d);\n", x, y);
      fprintf (stdout, "cairo_line_to(context, %d, %d + %.02f);\n", x, y, lenght);
      fprintf (stdout, "cairo_set_line_width(context, %.02f);\n", current * ratio);
      fprintf (stdout, "cairo_stroke(context);\n");
      */
      bar = 0;
    }
    else
      bar = 1;
    
    x += current * ratio;
    i++;
  }
  /* from:int svg_bars(struct Barcode_Item *bc, FILE *f) */

  *(output + size - 1) = '\0';
  data = strdup (output);
  free (output);
  output = NULL;

  return data;
}

char *
barcode_get_text_data (int type, char *code)
{
  int oflags = type | BARCODE_OUT_PS | BARCODE_OUT_NOHEADERS;
  struct Barcode_Item *Bar;
  Bar = Barcode_Create(code);
  if (Bar->error) return NULL;
  Barcode_Encode(Bar, oflags);
  return Bar->textinfo;
}

char *
render_iec16022 (char *grid, int i_width, int i_height, double w, double h)
{
   double ratio;
   double pixel;
   int i, j;
   int size;
   char *output;
   char *data;

   output = (char *) malloc (4096);
   size = 0;

   /* Treat requested size as a bounding box, scale to maintain aspect
    * ratio while fitting it in this bounding box. */
 	ratio = (double) i_height / (double) i_width;
   if (h > w * ratio)
      h = w * ratio;
   else
      w = h / ratio;

   /* Now determine pixel size. */
   pixel = w / i_width;
   if (pixel < MIN_PIXEL_SIZE) pixel = MIN_PIXEL_SIZE;

   /* Now traverse the code string and create a list of boxes */
   for (i = i_height-1; i >= 0; i--)
      for (j = 0; j < i_width; j++)
         if (*grid++)
         {
            double x = j * pixel + pixel / 2.0;
            double y = i * pixel;
            double length = pixel;
            double width  = pixel;

            sprintf (output + size, "%.02f:%.02f:%.02f:%.02f ", x, y, width, length);
            size = strlen (output);
            /*
            fprintf (stdout, "cairo_move_to (cr, %.02f, %.02f);\n", x, y);
            fprintf (stdout, "cairo_line_to (cr, %.02f, %.02f + %.02f);\n", x, y, length);
            fprintf (stdout, "cairo_set_line_width (cr, %.02f);\n", width);
            fprintf (stdout, "cairo_stroke (cr);\n");
            */
         }

   /* fill in other info */
   //double height = i_height * pixel;
   //double width  = i_width  * pixel;
  
   *(output + size - 1) = '\0';
   data = strdup (output);
   free (output);
   output = NULL;

   return data;
}

char *
datamatrix_get_code_data (int type, char *code, double width, double height)
{
   char *grid;
   int i_width;
   int i_height;

   if (strlen (code) == 0) return NULL;

   i_width  = 0;
   i_height = 0;

   grid = (char *) iec16022ecc200 (&i_width, &i_height, NULL, strlen (code), (unsigned char *) code,
                                   NULL, NULL, NULL);

   return render_iec16022 (grid, i_width, i_height, width, height);
}

char *
postnet_get_code_data (int type, const char *code, double width, double height)
{
   char *buffer;
   char *digit;
   char *output;
   char *data;
   double a;
   int size;

   output = (char *) malloc (2048);
   size = 0;

   /* Validate code length for all subtypes. */
   if (!check_valid_type (type, code)) return NULL;

   /* First get code string */
   buffer = postnet_code (code);
   if (buffer == NULL) return NULL;

   /* Now traverse the code string and create a list of lines */
   a = POSTNET_HORIZ_MARGIN;
   for (digit = buffer; *digit != 0; digit++)
   {
      double x = a;
      double y = POSTNET_VERT_MARGIN;
      double width = POSTNET_BAR_WIDTH;
      double length;

      if (*digit == '0')
      {
         y += POSTNET_FULLBAR_HEIGHT - POSTNET_HALFBAR_HEIGHT;
         length = POSTNET_HALFBAR_HEIGHT;
      } else
         length = POSTNET_FULLBAR_HEIGHT;

      sprintf (output + size, "%.02f:%.02f:%.02f:%.02f ", x, y, width, length);
      size = strlen (output);
      /*
      fprintf (stdout, "cairo_move_to (context, %.02f, %.02f);\n", x, y);
      fprintf (stdout, "cairo_line_to (context, %.02f, %.02f + %.02f);\n", x, y, length);
      fprintf (stdout, "cairo_set_line_width (context, %.02f);\n", width);
      fprintf (stdout, "cairo_stroke (context);\n");
      */

      a += POSTNET_BAR_PITCH;
   }

   //double width = a + POSTNET_HORIZ_MARGIN;
   //double height = POSTNET_FULLBAR_HEIGHT + 2 * POSTNET_VERT_MARGIN;

   *(output + size - 1) = '\0';
   data = strdup (output);
   free (output);
   output = NULL;

   return data;
}
