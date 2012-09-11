#include <stdlib.h>
#include <string.h>
#include "barcode.h"
#include "../barcode.h"

char *
get_code_data (int type, char *code, double width, double height)
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
      sprintf (output + size, "%d.0:%d.0:%.02f:%.02f|", x, y, current * ratio, lenght);
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
get_text_data (int type, char *code)
{
  int oflags = type | BARCODE_OUT_PS | BARCODE_OUT_NOHEADERS;
  struct Barcode_Item *Bar;
  Bar = Barcode_Create(code);
  if (Bar->error) return NULL;
  Barcode_Encode(Bar, oflags);
  return Bar->textinfo;
}
