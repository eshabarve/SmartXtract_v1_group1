from pdf2image import convert_from_bytes
from PIL import UnidentifiedImageError

def pdf_to_images(pdf_file):
    try:
        # Read file bytes
        try:
            pdf_bytes = pdf_file.read()
            if not pdf_bytes:
                raise ValueError("Empty PDF file.")
        except Exception as e:
            raise ValueError(f"Failed to read PDF file: {e}")
        
        # Convert PDF to Images
        try:
            images = convert_from_bytes(pdf_bytes, use_pdftocairo=True)
            if not images:
                raise ValueError("No pages found in PDF.")
        except FileNotFoundError:
            raise RuntimeError("'pdftocairo' not found. Please install poppler-utils.")
        except UnidentifiedImageError:
            raise RuntimeError("Could not interpret PDF as image.")
        except Exception as e:
            raise RuntimeError(f"Error converting PDF to images: {e}")
        
        # Return first page
        print(f"PDF converted successfully: {len(images)} page(s) found")
        return images[0]

    except Exception as e:
        print("Error in pdf_to_images:", str(e))
        raise
