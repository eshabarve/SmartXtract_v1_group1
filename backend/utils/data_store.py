import json
import csv
import re
import os

def data_storage_csv(company_name, document_type, structured_text):
    
    if not structured_text or not structured_text.strip():
        print("JSON Object/Array is empty. ")
        return []
    
    if not company_name or document_type:
        print("Module did not get either Company Name or Document Type. ")
        return []

    # Capture content between ```...``` or just raw JSON
    match = re.search(r"(\[.*\]|\{.*\})", structured_text, flags=re.DOTALL)
    if not match:
        print("No JSON object/array found in LLM output. ")
        print("Raw output:\n", structured_text)
        return []

    cleaned = match.group(1).strip()
    cleaned = cleaned.replace("“", "\"").replace("”", "\"")
    cleaned = cleaned.replace("‘", "'").replace("’", "'")

    try:
        structured_text = json.loads(cleaned)
    except json.JSONDecodeError as e:
        print("JSON parsing failed:", e)
        print("Extracted content after cleaning:\n", cleaned)
        return []
    
    # --- Ensure structured_text is list of dicts ---
    if isinstance(structured_text, dict):
        structured_text = [structured_text]

    if not (isinstance(structured_text, list) and all(isinstance(row, dict) for row in structured_text)):
        print("Invalid or empty data. No CSV file created. ")
        return []

    # Ensure output folder exists
    output_dir = "./DATA"
    company_dir = os.path.join(output_dir, company_name)    # CompanyName Directory in DATA directory
    doc_dir = os.path.join(company_dir, document_type)  # DocumenName Directory in Company directory
    os.makedirs(doc_dir, exist_ok=True)

    # Create Filename and store in document directory
    filename = f"{company_name}_{document_type}.csv".replace(" ", "_")
    filepath = os.path.join(doc_dir, filename)

    # Write to CSV
    headers = set()
    for row in structured_text:
        headers.update(row.keys())
    headers = list(headers)

    with open(filepath, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerow(row)

        print(f"CSV file saved as: {filepath}")