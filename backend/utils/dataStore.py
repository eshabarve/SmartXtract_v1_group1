import json
import csv
import re
import os

company_name = "ABC_Ltd"
document_type = "invoice"

def dataStorageCSV(company_name, document_type, structured_text):
    
    if not structured_text or not structured_text.strip():
        print("❌ JSON object/array is empty")
        return []

    # Regex: capture content between ```...``` or just raw JSON
    match = re.search(r"(\[.*\]|\{.*\})", structured_text, flags=re.DOTALL)
    if not match:
        print("❌ No JSON object/array found in LLM output")
        print("Raw output:\n", structured_text)
        return []

    cleaned = match.group(1).strip()
    cleaned = cleaned.replace("“", "\"").replace("”", "\"")
    cleaned = cleaned.replace("‘", "'").replace("’", "'")

    try:
        structured_text = json.loads(cleaned)
    
    except json.JSONDecodeError as e:
        print("❌ JSON parsing failed:", e)
        print("Extracted content after cleaning:\n", cleaned)
        return []

    # Ensure output folder exists (optional)
    output_dir = "./DATA/ABC_Ltd/invoice"
    os.makedirs(output_dir, exist_ok=True)

    # Create a filename using company name and document type
    filename = f"{company_name}_{document_type}.csv"
    filepath = os.path.join(output_dir, filename)

    # Write to CSV
    if structured_text and isinstance(structured_text, list) and all(isinstance(row, dict) for row in structured_text):
        # Get headers from keys of first row
        headers = ["Part", "Quantity", "Price"]

        with open(filepath, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(structured_text)

        print(f"CSV file saved as: {filepath}")

    else:
        print("Invalid or empty data. No CSV file created.")