import traceback
from flask import Flask, request
from utils.pdf_to_image import pdf_to_images
from utils.img_prep_process import img_process
from utils.ocr_extraction import ocr_extraction
from utils.prompt_generator import generate_prompt
from utils.llm_module import llm_structuring
# from utils.conf_score import conf_scoring
from utils.data_store import data_storage_csv
# from utils.integration import intgrtIntoEntpriceSys


app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def extract_data():
    
     try:
          # Getting Files, Compan Name, Document Type
          file = request.files.get('file')
          print("File received:", file.filename)
          company_name = request.form.get('company_name')
          print("Company Name:", company_name)
          document_type = request.form.get('document_type')
          print("Document Type:", document_type)

          if not file:
               return {"error": "No file received"}, 400
          
          if not company_name or not document_type:
               return {"error": "company_name and document_type are required"}, 400
          

          #PDF to Image Module
          # poppler_path=r"poppler\Library\bin"
          img=pdf_to_images(file)
          print("Converted PDF into Image")

          # Image Pre-Processing Module
          clean_img = img_process(img)
          print("Output of imgProcess:", type(clean_img), clean_img)

          # OCR Extraction Module
          extracted_text= ocr_extraction(clean_img)
          print("Output of ocr_extraction:", type(extracted_text), extracted_text)
          
          # Prompt generator Module
          prompt = generate_prompt(company_name, document_type, extracted_text)

          # LLM Structuring Module
          structured_text = llm_structuring(extracted_text, prompt)
          print("Output of llmStructuring:", type(structured_text), structured_text)

          # Data Storage Module
          data_storage_csv(company_name, document_type, structured_text)
          print("Data is stored")
          return {"status": "done"}

     except Exception as e:
          tb = traceback.format_exc()
          print("Error in Flask endpoint:\n", tb)
          return {"error": str(e), "traceback": tb}, 500



if __name__ == "__main__":
     app.run(debug=True)