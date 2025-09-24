import cv2
import numpy as np
from PIL import Image

def imgProcess(images):
     
     img = Image.open(images).convert("RGB")
     cvImage = np.array(img)    # Converting to numpy image
     cvImage = cv2.cvtColor(cvImage, cv2.COLOR_RGB2BGR)     # Converting from RGB to BGR
     gray = cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)     # Converting from BGR to Gray
     # denoised = cv2.medianBlur(gray, 3)     # Denoising using median blur
     thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)     # Binarizing Image
     print("✅ imgProcess: shape =", thresh.shape, "dtype =", thresh.dtype)
     pil_img = Image.fromarray(thresh)
     return pil_img



# img_path = r"C:\Users\Nitin\Downloads\ABC_Ltd_Bill of materials_1.jpg"
# img = cv2.imread(img_path)
# pre_procssed_image = imgProcess(img)
# cv2.imshow("", pre_procssed_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()