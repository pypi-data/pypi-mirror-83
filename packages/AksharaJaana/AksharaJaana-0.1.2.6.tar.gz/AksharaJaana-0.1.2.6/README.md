# AksharaJaana

AksharaJaana is the package which uses tesseract ocr in backend to convert the kannada text to editable format.You can use
following sample code in ubuntu.The Special feature of this is it can separate columns in page

# Sample Code 

## Installing the AksharaJaana

### pip install AksharaJaana



## Python Script

import AksharaJaana.main as ak 
text = ak.ocr_engine('/home/navaneeth/Desktop/NandD/OCR_kannada/CamScanner 06-28-2020 12.12.10.pdf')

from AksharaJaana.utils import utils
u = utils()
u.write_as_RTF(text, saving_path='/home/navaneeth/Desktop/1.rtf')


