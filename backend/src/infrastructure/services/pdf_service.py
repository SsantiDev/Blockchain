from fpdf import FPDF
from datetime import datetime
import io
import os

class PDFCertificateGenerator:
    """
    Infrastructure service to generate Notarization Certificates in PDF format.
    """
    
    def generate_certificate(self, transaction_data: dict) -> io.BytesIO:
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        
        # --- Header ---
        pdf.set_fill_color(20, 22, 32) # Dark background matching the brand
        pdf.rect(0, 0, 210, 40, 'F')
        
        pdf.set_font("Arial", 'B', 24)
        pdf.set_text_color(0, 255, 204) # Accent color
        pdf.cell(0, 20, "NOTARYCHAIN", ln=True, align='C')
        
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 5, "Certificate of Notarization", ln=True, align='C')
        
        pdf.ln(20)
        
        # --- Body ---
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Document Verification Record", ln=True)
        pdf.ln(5)
        
        pdf.set_font("Arial", '', 11)
        
        # Helper to add fields
        def add_field(label, value):
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(40, 8, f"{label}:", 0)
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 8, str(value))
            pdf.ln(2)

        timestamp = transaction_data.get('timestamp', 0)
        dt_object = datetime.fromtimestamp(timestamp)
        formatted_date = dt_object.strftime("%Y-%m-%d %H:%M:%S UTC")

        add_field("Owner Address", transaction_data.get('owner', 'N/A'))
        add_field("Date & Time", formatted_date)
        add_field("Document Hash", transaction_data.get('document_hash', 'N/A'))
        
        metadata = transaction_data.get('metadata', {})
        add_field("Original Name", metadata.get('original_filename', 'Unknown'))
        add_field("Description", metadata.get('description', 'No description provided'))
        
        pdf.ln(10)
        
        # --- Blockchain Proof ---
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Blockchain Integrity Proof", ln=True)
        pdf.ln(2)
        
        pdf.set_font("Courier", '', 9)
        pdf.set_fill_color(240, 240, 240)
        pdf.multi_cell(0, 8, f"Digital Signature:\n{transaction_data.get('signature', 'N/A')}", border=1, fill=True)
        
        pdf.ln(20)
        
        # --- Footer ---
        pdf.set_y(-50)
        pdf.set_font("Arial", 'I', 8)
        pdf.set_text_color(100, 100, 100)
        footer_text = (
            "This document serves as cryptographic proof that the mentioned file existed in its current state "
            "at the specified time. Any change to the original file will invalidate this certificate."
        )
        pdf.multi_cell(0, 5, footer_text, align='C')
        
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 10)
        pdf.set_text_color(20, 22, 32)
        pdf.cell(0, 10, "Verify at: https://notarychain.commercial.app", ln=True, align='C')
        
        # Output as bytes
        output = io.BytesIO()
        pdf_content = pdf.output()
        output.write(pdf_content)
        output.seek(0)
        
        return output
