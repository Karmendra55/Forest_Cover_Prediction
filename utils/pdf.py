from fpdf import FPDF
import tempfile
import matplotlib.pyplot as plt
from datetime import datetime
import os
from utils.logger import log_error

def generate_single_patch_pdf(user_inputs, predicted_class, predicted_name, probabilities, cover_type_map, charts=None):
    charts = charts or []
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
     # --- HEADER ---
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(34, 85, 34)
    pdf.cell(0, 10, "Forest Cover Type Prediction Report", ln=True, align="C")
    pdf.set_draw_color(34, 85, 34)
    pdf.set_line_width(0.5)
    pdf.line(10, 25, 200, 25) 
    pdf.ln(10)
    
    # --- Timestamp ---
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, f"Generated on: {timestamp}", ln=True, align="R")
    pdf.ln(5)
    
    # --- Prediction Summary ---
    pdf.set_font("Arial", "B", 13)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Prediction Summary", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, f"Predicted Cover Type: {predicted_class} - {predicted_name}")
    pdf.ln(5)
    
    # --- Input Parameters ---
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, "Input Parameters", ln=True)
    pdf.set_font("Arial", "", 11)
    
    col_width = 65
    row_height = 8
    if user_inputs:
        for key, value in user_inputs.items():
            pdf.set_fill_color(245, 245, 245)
            pdf.cell(col_width, row_height, str(key), border=1, fill=True)
            pdf.cell(0, row_height, str(value), border=1, ln=True)
    else:
        pdf.multi_cell(0, 8, "No inputs saved for this record.")
    pdf.ln(8)
    
    # --- PROBABILITY BAR CHART ---
    probs = list(probabilities) if probabilities is not None else []
    if len(probs) > 0:
        labels = [cover_type_map.get(i + 1, str(i + 1)) for i in range(len(probs))]
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.barh(labels, probs)
        ax.set_xlabel("Probability")
        ax.set_title("Prediction Probabilities")
        plt.tight_layout()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            plt.savefig(tmpfile.name, format="PNG", bbox_inches="tight")
            plt.close(fig)
            pdf.image(tmpfile.name, x=30, w=150)
        pdf.ln(10)

    if charts:
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, "Additional Charts", ln=True)
        for img_path in charts:
            if img_path and os.path.exists(img_path):
                pdf.image(img_path, x=30, w=150)
                pdf.ln(10)
    
    # --- footers ---
    pdf.set_y(-20)
    pdf.set_font("Arial", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 10, "Forest Cover Prediction System © 2025", align="C")
    
    output = pdf.output(dest="S")
    if isinstance(output, str):
        pdf_bytes = output.encode("latin-1")
    else:
        pdf_bytes = bytes(output)
    return pdf_bytes
