from fpdf import FPDF

# Step 1: Load the structured JSON file containing the extracted text data
with open('structured-text-data.json', 'r') as f:
    data = json.load(f)

# Step 2: Extract the text content and remove duplicates
unique_texts = set()  # Use a set to automatically handle duplicates

for item in data.get('data', []):
    text_content = item.get('content', '').strip()
    if text_content:
        unique_texts.add(text_content)  # Add text to the set, duplicates will be ignored

# Step 3: Combine the unique text parts into a single string
combined_text = '\n\n'.join(unique_texts)

# Step 4: Write the combined text into a PDF file using FPDF with UTF-8 support
pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# Use a font that supports UTF-8 characters
pdf.set_font("Arial", size=12)

for line in combined_text.split('\n\n'):
    pdf.multi_cell(0, 10, line)
    pdf.ln()

# Step 5: Save the PDF file
output_pdf = 'combined_text.pdf'
pdf.output(output_pdf)

print(f"Combined PDF has been saved to {output_pdf}")
