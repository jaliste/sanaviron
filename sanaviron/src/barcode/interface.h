#include "barcode.h"
#include "postnet.h"
#include "iec16022ecc200.h"

#define DATAMATRIX 20

char *barcode_get_code_data (int type, char *code, double width, double height);
char *barcode_get_text_data (int type, char *code);
char *datamatrix_get_code_data (int type, char *code, double width, double height);
char *postnet_get_code_data (int type, char *code, double width, double height);
