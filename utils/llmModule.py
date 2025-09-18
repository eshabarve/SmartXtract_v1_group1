import ollama

text = '''Tesseract Output:
Part Quantity Price

Drill motor 1 $99.00
PLA filament ~400 g 1 $10.00
NinjaFlex filament ~20 g 1 $1.60
12-V DC motor 200 rpm 1 $14.99
Caster bearings 3 $2.99
Speed controller 1 $8.45
Power supply 1 $15.84
1” Forstner bit 1 $11.75
18 AWG hookup wire pack 1 $14.99
3/8"'-16 x 1.25” in bolt 1 $0.32
3/8''-16 regular hex nut 1 $0.05
M3 hex nut 3 $0.03
MB grub screw 3 $0.29
M3 heat insert 20 $2.46
M5 heat insert 4 $0.91
M3 x 10 screw 25 $1.36'''

prompt = '''
You are an intelligent assistant that extracts structured information from OCR scanned invoices or receipts or purchase.

Given OCR text that lists parts, quantities, and prices extract each item into the format:

Part | Quantity | Price

Each row represents:
- Part: The name or description of the item
- Quantity: A number
- Price: In dollars

Extract Part, Quantity, and Price from this OCR text.Just return the JSON list of objects, no explanation.

OCR Text:
# {text}
Part Quantity Price

Drill motor 1 $99.00
PLA filament ~400 g 1 $10.00
NinjaFlex filament ~20 g 1 $1.60
12-V DC motor 200 rpm 1 $14.99
Caster bearings 3 $2.99
Speed controller 1 $8.45
Power supply 1 $15.84
1” Forstner bit 1 $11.75
18 AWG hookup wire pack 1 $14.99
3/8"'-16 x 1.25” in bolt 1 $0.32
3/8''-16 regular hex nut 1 $0.05
M3 hex nut 3 $0.03
MB grub screw 3 $0.29
M3 heat insert 20 $2.46
M5 heat insert 4 $0.91
M3 x 10 screw 25 $1.36
'''


response = ollama.chat(
    model='llama3.1',
    messages=[
        {"role": "user", "content": prompt}
    ],
    
)

print(response['message']['content'])