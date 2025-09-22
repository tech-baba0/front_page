from flask import Flask, render_template, request, send_file
from weasyprint import HTML
from io import BytesIO
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    # Show your front page maker form
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    form = request.form
    data = {
        "subject": form.get("subject", ""),
        "title": form.get("title", ""),
        "submitted_to": form.get("submitted_to", ""),
        "submitted_by": form.get("submitted_by", ""),
        "footer": form.get("footer", ""),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Render filled-in HTML
    rendered = render_template("preview.html", **data)

    # Convert HTML to PDF
    pdf_bytes = BytesIO()
    HTML(string=rendered).write_pdf(pdf_bytes)
    pdf_bytes.seek(0)

    return send_file(
        pdf_bytes,
        as_attachment=True,
        download_name="frontpage.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)
