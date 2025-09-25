

def generate_prompt(company_name, document_type, extracted_text):

     base_instructions =f"""
     You are an intelligent assistant that extracts structured information from OCR scanned **{document_type}** documents of {company_name}.
     Your job is to produce a clean JSON array of objects.
     Each object should have consistent keys across rows.
     If any field is missing or not found, set it to null (lowercase, valid JSON).
     Do not include any explaination, only JSON.
     Use double quotes for keys and values.
     """

     doc_fields ={
          "invoice": ["Part", "Quantity", "Price"],
     }

     # if not document_type:

     fields = doc_fields.get(document_type.lower(), ["Field1", "Field2", "Field3"])
     fields_str = " | ".join(fields)
     field_instructions =f"""Expected fields per row: {fields_str}
     Rules:
     - Maintain these keys exactly.
     - If value is missing or unclear, assign Null.
     - use Double quotes for keys and values.
     """
     prompt = f"""{base_instructions}
{field_instructions}
OCR Text:{extracted_text}

"""

     return prompt