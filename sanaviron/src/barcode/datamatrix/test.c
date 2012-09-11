#include <stdio.h>
#include <stdlib.h>
#include "../barcode.h"

int
main (int argc, char *argv[])
{
   fprintf (stdout, "%s\n", get_code_data (DATAMATRIX, "sanaviron", 100.0, 100.0));
	
   exit (EXIT_SUCCESS);
}
