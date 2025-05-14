from fpdf import FPDF

def create_pdf_from_text(input_file, output_file):
    # Read the text file
    with open(input_file, 'r') as file:
        content = file.read()
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Split content into lines
    lines = content.split('\n')
    
    # Process each line
    for line in lines:
        # Check if line is a heading
        if line.startswith('# '):
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, line[2:], ln=True)
            pdf.ln(5)
        elif line.startswith('## '):
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, line[3:], ln=True)
            pdf.ln(5)
        elif line.startswith('### '):
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, line[4:], ln=True)
            pdf.ln(5)
        elif line.startswith('**'):
            # Bold text
            pdf.set_font("Arial", 'B', 12)
            clean_line = line.replace('**', '')
            pdf.cell(0, 10, clean_line, ln=True)
            pdf.set_font("Arial", size=12)
        elif line.strip() == '':
            # Empty line
            pdf.ln(5)
        else:
            # Regular text
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, line)
    
    # Save the pdf
    pdf.output(output_file)

if __name__ == "__main__":
    create_pdf_from_text("knowledge_base/sample_mental_health_info.txt", "knowledge_base/mental_health_coping_strategies.pdf")
    print("PDF created successfully!")
