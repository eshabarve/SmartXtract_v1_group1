
def pdf_to_images(pdf_file):
    """
    Converts a PDF file-like object into a list of PIL Image objects.
    """
    from pdf2image import convert_from_bytes

    pdf_bytes = pdf_file.read()
    images = convert_from_bytes(pdf_bytes, use_pdftocairo=True)

    return images[0] 