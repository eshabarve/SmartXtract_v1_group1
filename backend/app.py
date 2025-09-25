import traceback
from flask import Flask, request, jsonify
from PIL import Image
from utils.initial_file_handling import handle_file
from utils.PDF_to_image import pdf_to_images
from utils.imgPrepProcess import imgProcess
from utils.OCR_Extraction import ocr_extraction
from utils.llmModule import llmStructuring
# from utils.confModule import confScoring
from utils.dataStore import dataStorageCSV
# from utils.integration import intgrtIntoEntpriceSys


app = Flask(__name__)

@app.route('/', methods=['GET','POST'])

def extract_data():
    
     try:
          # Getting Files, Compan Name, Document Type
          file = request.files.get('file')
          company_name = request.form.get('company_name')
          document_type = request.form.get('document_type')

          if not file:
               return {"error": "No file received"}, 400
          
          if not company_name and not document_type:
               return {"error": "company_name and document_type are required"}, 400
          
          print("File received:", file.filename)
          print("Company Name:", company_name)
          print("Document Type:", document_type)



          filename = file.filename.lower()

          if filename.endswith(".pdf"):
            
            img = pdf_to_images(file)   # returns PIL image
            print("📄 PDF converted to image")

          elif filename.endswith((".jpg", ".jpeg", ".png")):
            # Directly open image files
            img = Image.open(file).convert("RGB")
            print("🖼️ Image file was recieved")
          else:
            return jsonify({"error": "Unsupported file type"}), 400


          #img=pdf_to_images(file)
          #print("pdf to images done!!")

          #PDF to Image Module
          # poppler_path=r"poppler\Library\bin"
          img=pdf_to_images(file)
          print("Converted PDF into Image")


          # Image Pre-Processing Module
          clean_img = imgProcess(img)
          print("Output of imgProcess:", type(clean_img), clean_img)

          # OCR Extraction Module
          extracted_text= ocr_extraction(clean_img)
          print("Output of ocr_extraction:", type(extracted_text), extracted_text)

          # LLM Structuring Module
          prompt = f'''You are an intelligent assistant that extracts structured information from OCR scanned invoices or receipts or purchase.

               Given OCR text that lists parts, quantities, and prices extract each item into the format:

               Part | Quantity | Price

               Each row represents:
               - Parts: The name or description of the item
               - Quantity: A number
               - Price: In dollars

               Rules:
               - Extract Part, Quantity, and Price from this OCR text. Always output a valid JSON list.
               - If a value is not found, set it explicitly to null.
               - Remove or replace unwanted characters such as ", ”, ‘, ’, “ inside Part names with normal quotes.
               - Do not include explanations, only return the JSON.

               OCR Text:
               # {extracted_text}
          '''
          structured_text = llmStructuring(extracted_text, prompt)
          print("Output of llmStructuring:", type(structured_text), structured_text)

          # Data Storage Module
          dataStorageCSV(company_name, document_type, structured_text)
          print("Data is stored")
          return {"status": "done"}

     except Exception as e:
          tb = traceback.format_exc()
          print("❌ Error in Flask endpoint:\n", tb)
          return {"error": str(e), "traceback": tb}, 500



if __name__ == "__main__":
     app.run(debug=True)