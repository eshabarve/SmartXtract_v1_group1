import json
import csv
import os

company_name = "ABC_Ltd"
document_type = "invoice"

# Extracted content (JSON in string format)
data = [
  {
    "Part": "Drill motor",
    "Quantity": "1",
    "Price": "$99.00"
  },
  {
    "Part": "PLA filament ~400 g",
    "Quantity": "1",
    "Price": "$10.00"
  },
  {
    "Part": "NinjaFlex filament ~20 g",
    "Quantity": "1",
    "Price": "$1.60"
  },
  {
    "Part": "12-V DC motor 200 rpm",
    "Quantity": "1",
    "Price": "$14.99"
  },
  {
    "Part": "Caster bearings",
    "Quantity": "3",
    "Price": "$2.99"
  },
  {
    "Part": "Speed controller",
    "Quantity": "1",
    "Price": "$8.45"
  },
  {
    "Part": "Power supply",
    "Quantity": "1",
    "Price": "$15.84"
  },
  {
    "Part": "1” Forstner bit",
    "Quantity": "1",
    "Price": "$11.75"
  },
  {
    "Part": "18 AWG hookup wire pack",
    "Quantity": "1",
    "Price": "$14.99"
  },
  {
    "Part": "3/8''-16 x 1.25” in bolt",
    "Quantity": "1",
    "Price": "$0.32"
  },
  {
    "Part": "3/8''-16 regular hex nut",
    "Quantity": "1",
    "Price": "$0.05"
  },
  {
    "Part": "M3 hex nut",
    "Quantity": "3",
    "Price": "$0.03"
  },
  {
    "Part": "MB grub screw",
    "Quantity": "3",
    "Price": "$0.29"
  },
  {
    "Part": "M3 heat insert",
    "Quantity": "20",
    "Price": "$2.46"
  },
  {
    "Part": "M5 heat insert",
    "Quantity": "4",
    "Price": "$0.91"
  },
  {
    "Part": "M3 x 10 screw",
    "Quantity": "25",
    "Price": "$1.36"
  }
]

# Ensure output folder exists (optional)
output_dir = "./DATA/ABC_Ltd/invoice"
os.makedirs(output_dir, exist_ok=True)

# Create a filename using company name and document type
filename = f"{company_name}_{document_type}.csv"
filepath = os.path.join(output_dir, filename)

# Write to CSV
if data and isinstance(data, list) and all(isinstance(row, dict) for row in data):
    # Get headers from keys of first row
    headers = ["Part", "Quantity", "Price"]

    with open(filepath, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    print(f"CSV file saved as: {filepath}")
else:
    print("Invalid or empty data. No CSV file created.")