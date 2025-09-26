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

from PIL import Image, UnidentifiedImageError
import pytesseract
import io
import os

# Set path to Tesseract executable (adjust as per your system)
pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR\tesseract.exe"

def ocr_extraction(clean_img, psm=4, lang="hin"):
    """
    Extract text from a preprocessed PIL image using Tesseract OCR.

    Args:
        clean_img (PIL.Image): Preprocessed image
        psm (int): Page segmentation mode for Tesseract. Default is 4.
        lang (str): Language code (e.g., 'eng', 'hin'). Default is 'hin' for Hindi.

    Returns:
        str: Extracted text as a single string.
    """
    try:
        # Validate input 
        if clean_img is None:
            raise ValueError("No image provided for OCR.")
        if not isinstance(clean_img, Image.Image):
            raise TypeError(f"Expected a PIL.Image, got {type(clean_img)}")

        # Build Tesseract config
        custom_config = f'--psm {psm}'
        
        # Run OCR
        try:
            extracted_text = pytesseract.image_to_string(clean_img, config=custom_config, lang=lang)
        except pytesseract.pytesseract.TesseractNotFoundError:
            raise RuntimeError("Tesseract not found. Please install Tesseract OCR and set the correct path.")
        except Exception as e:
            raise RuntimeError(f"OCR failed: {e}")

        # Clean text 
        extracted_text = extracted_text.strip()

        print(f"OCR successful: {len(extracted_text)} characters extracted")
        return extracted_text

    except Exception as e:
        print("Error in ocr_extraction:", str(e))
        raise
