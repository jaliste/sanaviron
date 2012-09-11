#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "postnet.h"

char *
get_code_data (int type, const char *code, double width, double height)
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

      sprintf (output + size, "%.02f:%.02f:%.02f:%.02f|", x, y, width, length);
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
