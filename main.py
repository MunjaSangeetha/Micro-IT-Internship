from flask import Flask, request, send_file
from fpdf import FPDF
import io
import os

app = Flask(__name__)

class PDF(FPDF):
    pass

@app.route('/generate-offer-letter', methods=['POST'])
def generate_offer_letter():
    name = request.form.get('name')
    position = request.form.get('position')
    joining_date = request.form.get('joining_date')
    salary = request.form.get('salary')

    pdf = PDF()
    pdf.add_page()

    # ✅ Load DejaVuSans.ttf from the current folder
    font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
    print("Font path:", font_path)
    print("Font file exists:", os.path.exists(font_path))  # Should print True

    if not os.path.exists(font_path):
        return "Font file not found. Please ensure DejaVuSans.ttf is in the same folder as main.py.", 500

    # ✅ Register and set the font
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", "", 12)

    # ✅ Write the content
    pdf.multi_cell(0, 10, f"""
Dear {name},

We are pleased to offer you the position of {position} at our company.

Your expected joining date is {joining_date}, and your annual salary will be ₹{salary}.

We are excited to have you on board and look forward to your valuable contribution.

Sincerely,
HR Department
""")

    # ✅ Stream PDF back to client
    pdf_output = pdf.output(dest='S').encode('latin1')
    pdf_buffer = io.BytesIO(pdf_output)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"Offer_Letter_{name}.pdf",
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)
