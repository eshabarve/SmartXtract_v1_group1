from pdf2image import convert_from_path

poppler_path = r"C:\poppler\poppler-25.07.0\Library\bin"

# Convert PDF pages to images
images = convert_from_path("Downloads/Onion_pvt_ltd_invoice_1.pdf", poppler_path=poppler_path, use_pdftocairo=True)

# Save first page as PNG
images[0].save("page1.png", "PNG")
print("PDF converted to image!!")

from IPython.display import display
display(images[0])