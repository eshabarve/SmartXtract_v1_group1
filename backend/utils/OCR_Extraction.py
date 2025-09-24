from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en') # 'use_angle_cls=True' helps with rotated text
img_path = "page1.png" # Replace with the actual path to your PNG image
result = ocr.predict(img_path) # 'cls=False' if angle classification is not needed 
print(result)

if result and "rec_texts" in result[0]:
    texts = result[0]["rec_texts"]
    print(texts)  # Prints the list of extracted texts
else:
    print("No text detected")


final_output= " ".join(texts)
print(final_output)