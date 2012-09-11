#include <stdlib.h>
#include <stdio.h>
#include "../barcode.h"

int
main (int argc, char *argv[])
{
	fprintf (stdout, "%s\n", get_code_data (POSTNET_9, "55555-1237", 100.0, 100.0));

	exit (EXIT_SUCCESS);
}
