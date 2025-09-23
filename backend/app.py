from flask import Flask, request

from utils.PDF_to_image import pdf_to_images
from utils.imgPrepProcess import imgProcess
# from utils.ocrExtraction import extractOCRText
from utils.llmModule import llmStructuring
# from utils.confModule import confScoring
# from utils.dataStore import dataStorageCSV
# from utils.integration import intgrtIntoEntpriceSys


app = Flask(__name__)

@app.rout('/')
def message():
     return None

@app.route('/extract', methods=['POST'])

def extract_data():
     file = request.files['file']
     poppler_path=r"poppler\Library\bin"
     img=pdf_to_images(file,poppler_path)
     clean_img = imgProcess(file)
     structured_text = llmStructuring()


if __name__ == "__main__":
     app.run(debug=True)