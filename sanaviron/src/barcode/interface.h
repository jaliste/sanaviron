#include "barcode.h"
#include "postnet.h"
#include "qrencode.h"
#include "iec16022ecc200.h"

#define DATAMATRIX 20
#define QR 21

char *barcode_get_code_data (int type, char *code, double width, double height);
char *barcode_get_text_data (int type, char *code);
char *qr_get_code_data (int type, char *code, double width, double height);
char *datamatrix_get_code_data (int type, char *code, double width, double height);
char *postnet_get_code_data (int type, char *code, double width, double height);
