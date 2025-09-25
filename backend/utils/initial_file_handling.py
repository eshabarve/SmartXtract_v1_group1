from pdf2image import convert_from_bytes
from PIL import Image

def handle_file(file):
    """
    Takes an uploaded file (PDF or image) and returns a single PIL image.
    - If PDF: converts the first page to an image
    - If JPG/PNG: opens directly as an image
    """
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        img = pdf_to_images(file)
        #return images[0]   # first page only
    
    elif filename.endswith((".jpg", ".jpeg", ".png")):
        img = Image.open(file).convert("RGB")
        return img
    
    else:
        raise ValueError("❌ Unsupported file type. Please upload a PDF, JPG, or PNG.")
