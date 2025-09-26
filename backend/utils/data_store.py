import json
import csv
import os

def data_storage_csv(company_name: str, document_type: str, llm_structured_text: dict):
    """
    Stores LLM structured JSON output (table) into a CSV file inside ./DATA/<Company>/<DocumentType>/.
    
    Args:
        company_name (str): Name of the company.
        document_type (str): Type of document (e.g., invoice).
        llm_structured_text (dict): LLM output with keys {"table": [...], "confidence": float, "flags": [...]}

    Returns:
        str | list: Path to saved CSV file or [] if failed.
    """
    try:
        if not company_name or not document_type:
            print("Missing Company Name or Document Type.")
            return []

        # Extract table
        try:
            table = llm_structured_text.get("table", [])
        except Exception as e:
            print(f"[Error] Unable to extract 'table' from LLM output: {e}")
            table = []

        if not table or not isinstance(table, list) or not all(isinstance(row, dict) for row in table):
            print("'table' is empty or invalid. No CSV created.")
            return []

        # Create folder structure
        output_dir = "./DATA"
        company_dir = os.path.join(output_dir, company_name)
        doc_dir = os.path.join(company_dir, document_type)
        os.makedirs(doc_dir, exist_ok=True)

        # Save to CSV
        filename = f"{company_name}_{document_type}.csv".replace(" ", "_")
        filepath = os.path.join(doc_dir, filename)

        # Collect headers from all rows
        headers = {key for row in table for key in row.keys()}
        headers = list(headers)

        try:
            with open(filepath, mode="w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                for row in table:
                    writer.writerow(row)
        except Exception as e:
            print(f"[Error] Writing CSV failed: {e}")
            return []

        print(f"CSV file saved as: {filepath}")
        return filepath

    except Exception as e:
        print(f"[Error] Unexpected error in data_storage_csv: {e}")
        return []
