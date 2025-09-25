

def generate_prompt(company_name, document_type, extracted_text):

     base_instructions =f"""
     You are an intelligent assistant that extracts structured information from OCR scanned **{document_type}**.
     Your job is to produce a clean JSON array of objects.
     Each object should have consistent keys across rows.
     If a field is missing in OCR, set is as Null.
     Do not include any explaination, only JSON.

     """

     return prompt