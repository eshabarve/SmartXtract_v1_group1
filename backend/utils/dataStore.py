import json
import csv
import os

company_name = "ABC_Ltd"
document_type = "invoice"

def dataStorageCSV(company_name, document_type, structured_text):
    
    structured_text = json.loads(structured_text)

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