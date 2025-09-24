
def pdf_to_images(file):
    """
    Converts a PDF file-like object into a list of PIL Image objects.
    """
    from pdf2image import convert_from_bytes

    pdf_bytes = file.read()
    images = convert_from_bytes(pdf_bytes, use_pdftocairo=True)

    return images 
