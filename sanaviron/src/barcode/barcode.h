/*
 * barcode.h -- GNU barcode/ECC200 ISO/IEC16022/POSTNET interface for Python
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
#include "postnet/postnet.h"
#include "lineal/barcode.h"
#include "datamatrix/iec16022ecc200.h"

#define DATAMATRIX 20

/*
enum {
   BARCODE_ANY = 0, // Choose best-fit
   BARCODE_EAN,     // Code EAN
   BARCODE_UPC,     // UPC == 12-digit EAN
   BARCODE_ISBN,    // ISBN numbers (still EAN13)
   BARCODE_39,      // Code 39
   BARCODE_128,     // Code 128 (a,b,c: autoselection)
   BARCODE_128C,    // Code 128 (compact form for digits)
   BARCODE_128B,    // Code 128, full printable ASCII
   BARCODE_I25,     // Interleaved 2 of 5 (only digits)
   BARCODE_128RAW,  // Raw code 128 (by Leonid A. Broukhis)
   BARCODE_CBR,     // Codabar (by Leonid A. Broukhis)
   BARCODE_MSI,     // MSI (by Leonid A. Broukhis)
   BARCODE_PLS,     // Plessey (by Leonid A. Broukhis)
   BARCODE_93,      // Code 93 (by Nathan D. Holmes)
   POSTNET = 15,    // Any of 5, 9 or 11 digits POSTNET
   POSTNET_5,       // 5 digits POSTNET
   POSTNET_6,       // 6 digits POSTNET
   POSTNET_9,       // 9 digits POSTNET
   POSTNET_11,      // 11 digits POSTNET
   CEPNET,          // 8 digits POSTNET (also known as CEPNET)
   DATAMATRIX = 20  // 2D dama matrix ECC200 ISO/IEC16022
};
*/

char *get_code_data (int type, char *code, double width, double height);
char *get_textinfo(int type, char *code);
