import cv2
import numpy as np
from PIL import Image, UnidentifiedImageError

def img_process(images):
    try:
        # Convert to RGB
        try:
            images = images.convert("RGB")
        except UnidentifiedImageError:
            raise ValueError("Invalid image format. Could not convert to RGB.")
        
        # Convert PIL -> NumPy -> OpenCV
        try:
            cv_image = np.array(images)
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
        except Exception as e:
            raise RuntimeError(f"Error converting image to OpenCV format: {e}")
        
        # Grayscale Conversion
        try:
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        except Exception as e:
            raise RuntimeError(f"Error converting image to grayscale: {e}")
        
        # Adaptive Thresholding ( Binarization )
        try:
            thresh = cv2.adaptiveThreshold(
                gray, 
                255, 
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 
                11, 
                2
            )
        except Exception as e:
            raise RuntimeError(f"Error during thresholding: {e}")

        # Convert back to PIL
        try:
            pil_img = Image.fromarray(thresh)
        except Exception as e:
            raise RuntimeError(f"Error converting processed image back to PIL: {e}")

        # Debug print
        print("imgProcess successful: shape =", thresh.shape, "dtype =", thresh.dtype)
        return pil_img
    
    except Exception as e:
        print("Error in img_process:", str(e))
        raise
