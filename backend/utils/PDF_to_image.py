
def pdf_to_images(pdf_path):
   
    from pdf2image import convert_from_path  # import inside function

    images = convert_from_path(pdf_path, poppler_path=poppler_path, use_pdftocairo=True)
    output_files = []

    for i, img in enumerate(images):
        filename = f"{output_prefix}_{i+1}.png"
        img.save(filename, "PNG")
        output_files.append(filename)

    return output_files 