def generate_prompt(company_name, document_type, extracted_text):
    """
    Generate a structured prompt for LLM based on company, document type, and OCR text.

    Args:
        company_name (str): Name of the company.
        document_type (str): Type of the document (e.g., 'Invoice').
        extracted_text (str): OCR-extracted raw text.

    Returns:
        str: A formatted prompt string for the LLM.
    """

    try:
        # Validate inputs
        if not company_name:
            raise ValueError("company_name is required to generate a prompt.")
        if not document_type:
            raise ValueError("document_type is required to generate a prompt.")
        if not extracted_text:
            raise ValueError("extracted_text is empty. OCR may have failed.")

        # Base instructions
        base_instructions = f"""
You are an intelligent assistant that extracts structured information from OCR scanned **{document_type}** documents of {company_name}. Your output MUST BE strictly valid JSON, nothing else. Do NOT include any explanations, markdown, or text outside JSON. The JSON object must have this structure:
{{
  "table": [ list of row objects ],
  "confidence": float between 0.0 and 1.0,
  "flags": [ list of warning strings if any issues ]
}}

Rules for "table":
- Each object in the array represents a row.
- Each object should have the same keys across rows.
- If a value is missing or unclear, set it to null.
- Use double quotes for keys and values.
- Do NOT include explanations or text outside JSON.

Rules for "confidence":
- Estimate how confident you are that the extraction is correct (0.0 to 1.0).

Rules for "flags":
- If you notice inconsistencies (e.g. missing fields, OCR errors), add them as strings in this array.
- Otherwise, return an empty array [].
"""

        # Expected fields based on document_type
        doc_fields = {
            "invoice": ["Part", "Quantity", "Price"],
        }

        fields = doc_fields.get(document_type.lower(), ["Field1", "Field2", "Field3"])
        fields_str = " | ".join(fields)

        field_instructions = f"""Expected fields per row: {fields_str}
Rules:
- Maintain these keys exactly.
- If value is missing or unclear, assign null.
- Use double quotes for keys and values.
"""

        # Build final prompt
        prompt = f"""{base_instructions}
{field_instructions}
OCR Text:
{extracted_text}
"""

        print(f"Prompt generated for {document_type} ({len(extracted_text)} OCR characters)")
        return prompt

    except Exception as e:
        print("Error in generate_prompt:", str(e))
        raise