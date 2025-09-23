from flask import Flask, request

#from utils.PDF_to_image import pdf_to_images
from utils.imgPrepProcess import imgProcess
from utils.OCR_Extraction import ocr_extraction
from utils.llmModule import llmStructuring
# from utils.confModule import confScoring
from utils.dataStore import dataStorageCSV
# from utils.integration import intgrtIntoEntpriceSys


app = Flask(__name__)
@app.route('/extract', methods=['GET', 'POST'])

def extract_data():

     if request.method == "GET":
        return {"message": "Use POST to upload files"}

     file = request.files['file']
     print("📂 File received:", file)

     #poppler_path=r"poppler\Library\bin"
     #img=pdf_to_images(file,poppler_path)

     clean_img = imgProcess(file)
     print("🖼️ Output of imgProcess:", type(clean_img), clean_img)

     extracted_text= ocr_extraction(clean_img)
     print("🔤 Output of ocr_extraction:", type(extracted_text), extracted_text)

     prompt = '''
    You are an intelligent assistant that extracts structured information from OCR scanned invoices or receipts or purchase.

    Given OCR text that lists parts, quantities, and prices extract each item into the format:

    Part | Quantity | Price

    Each row represents:
    - Part: The name or description of the item
    - Quantity: A number
    - Price: In dollars

    Extract Part, Quantity, and Price from this OCR text.Just return the JSON list of objects, no explanation.

    OCR Text:
    # {text}
    Part Quantity Price

    Drill motor 1 $99.00
    PLA filament ~400 g 1 $10.00
    NinjaFlex filament ~20 g 1 $1.60
    12-V DC motor 200 rpm 1 $14.99
    Caster bearings 3 $2.99
    Speed controller 1 $8.45
    Power supply 1 $15.84
    1” Forstner bit 1 $11.75
    18 AWG hookup wire pack 1 $14.99
    3/8"'-16 x 1.25” in bolt 1 $0.32
    3/8''-16 regular hex nut 1 $0.05
    M3 hex nut 3 $0.03
    MB grub screw 3 $0.29
    M3 heat insert 20 $2.46
    M5 heat insert 4 $0.91
    M3 x 10 screw 25 $1.36
    '''

     structured_text = llmStructuring(extracted_text, prompt)
     print("📑 Output of llmStructuring:", type(structured_text), structured_text)

     company_name = "ABC_Ltd"
     document_type = "invoice"
     dataStorageCSV(company_name, document_type, structured_text)

     return {"status": "done"}


if __name__ == "__main__":
     app.run(debug=True)