# from paddleocr import PaddleOCR
# ocr = PaddleOCR(use_angle_cls=True, lang='en') # 'use_angle_cls=True' helps with rotated text
# img_path = "page1.png" # Replace with the actual path to your PNG image
# result = ocr.predict(img_path) # 'cls=False' if angle classification is not needed 
# print(result)
# def ocr_extraction(img_path):
#     # Import inside the function
#     from paddleocr import PaddleOCR
#     # Initialize OCR engine
#     ocr = PaddleOCR(use_angle_cls=True, lang='en')  # handles rotated text
#     # Run OCR on the image
#     result = ocr.predict(img_path)  # 'cls=False' if angle classification is not needed
#     # Extract recognized text
#     if result and "rec_texts" in result[0]:
#         texts = result[0]["rec_texts"]
#         final_output = " ".join(texts)
#     else:
#         final_output = ""  # return empty string if no text detected
#     return final_output 

from PIL import Image
import pytesseract
import io

# Set path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR\tesseract.exe"

def ocr_extraction(clean_img, psm=3):
    """
    Extract text from an uploaded image file using Tesseract OCR.

    Args:
        file_obj: File object from Flask (request.files['file'])
        psm (int): Page segmentation mode for Tesseract. Default is 4.

    Returns:
        str: Extracted text as a single string.
    """
    # Tesseract config
    custom_config = f'--psm {psm}'

    # Run OCR
    extracted_text = pytesseract.image_to_string(clean_img, config=custom_config)

    # Clean text
    extracted_text = extracted_text.strip()

    return extracted_text
