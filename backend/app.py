import traceback
from PIL import Image, UnidentifiedImageError
from flask import Flask, request, jsonify
from utils.pdf_to_image import pdf_to_images
from utils.img_prep_process import img_process
from utils.ocr_extraction import ocr_extraction
from utils.prompt_generator import generate_prompt
from utils.llm_module import llm_structuring
from utils.conf_score import conf_scoring
from utils.data_store import data_storage_csv
# from utils.integration import intgrtIntoEntpriceSys


app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def extract_data():
    try:
        # Get input data
        file = request.files.get('file')
        company_name = request.form.get('company_name')
        document_type = request.form.get('document_type')

        if not file:
            return jsonify({"error": "No file received"}), 400
        if not company_name or not document_type:
            return jsonify({"error": "company_name and document_type are required"}), 400

        filename = file.filename.lower()
        print(f"File received: {filename}")
        print(f"Company Name: {company_name}")
        print(f"Document Type: {document_type}")

        # Convert PDF to image Module
        try:
            if filename.endswith(".pdf"):
                img = pdf_to_images(file)
                print("PDF converted to image")
            elif filename.endswith((".jpg", ".jpeg", ".png")):
                img = Image.open(file).convert("RGB")
                print("Image file was received")
            else:
                return jsonify({"error": "Unsupported file type"}), 400
        except UnidentifiedImageError:
            return jsonify({"error": "Could not process the image file"}), 400
        except Exception as e:
            tb = traceback.format_exc()
            print("Error in file conversion:\n", tb)
            return jsonify({"error": f"File conversion failed: {str(e)}", "traceback": tb}), 500

        # Preprocess Image Module
        try:
            clean_img = img_process(img)
            print("Image preprocessing successful")
        except Exception as e:
            tb = traceback.format_exc()
            print("Error in img_process:\n", tb)
            return jsonify({"error": f"Image preprocessing failed: {str(e)}", "traceback": tb}), 500

        # OCR Extraction Module
        try:
            ocr_extracted_text = ocr_extraction(clean_img)
            print("OCR extraction successful")
        except Exception as e:
            tb = traceback.format_exc()
            print("Error in ocr_extraction:\n", tb)
            return jsonify({"error": f"OCR extraction failed: {str(e)}", "traceback": tb}), 500

        # Prompt Generator Module
        try:
            prompt = generate_prompt(company_name, document_type, ocr_extracted_text)
            print("Prompt generation successful")
        except Exception as e:
            tb = traceback.format_exc()
            print("Error in generate_prompt:\n", tb)
            return jsonify({"error": f"Prompt generation failed: {str(e)}", "traceback": tb}), 500

        # LLM Structuring Module
        try:
            llm_structured_text = llm_structuring(prompt)
            if not llm_structured_text:
                return{
                    "status" : "failed",
                    "error" : "LLM output invalid or could not be parsed"
                }, 500
            else:
                print("LLM structuring successful")
        except Exception as e:
            tb = traceback.format_exc()
            print("Error in llm_structuring:\n", tb)
            return jsonify({"error": f"LLM structuring failed: {str(e)}", "traceback": tb}), 500
        
          # Confidence Scoring Module
        try:
            conf_scores = conf_scoring(ocr_extracted_text, llm_structured_text)
        except Exception as e:
          print(f"[Warning] Confidence scoring failed: {e}")
          conf_scores = {
               "row_score": [],
               "row_count_score": 0.0,
               "field_score": 0.0,
               "embed_score": 0.0,
               "llm_conf": 0.0,
               "final_conf": 0.0
          }
          
        # Data Storing Module
        try:
            result = data_storage_csv(company_name, document_type, llm_structured_text)
            if result:
                print("Data stored successfully:", result)
            else:
                print("Data was not stored, check data_store module.")
        except Exception as e:
            tb = traceback.format_exc()
            print("Error in data_storage_csv:\n", tb)
            return jsonify({"error": f"Data storage failed: {str(e)}", "traceback": tb}), 500

    except Exception as e:
        tb = traceback.format_exc()
        print("Unexpected Error in Flask endpoint:\n", tb)
        return jsonify({"error": f"Unexpected error: {str(e)}", "traceback": tb}), 500


if __name__ == "__main__":
    app.run(debug=True)