#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "iec16022ecc200.h"

#define MIN_PIXEL_SIZE 1.0

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

            sprintf (output + size, "%.02f:%.02f:%.02f:%.02f|", x, y, width, length);
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
barcode_iec16022 (double width, double height, char *code)
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
get_code_data (int type, char *code, double width, double height)
{
   return barcode_iec16022 (width, height, code);
}
