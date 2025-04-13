from flask import Flask, request, render_template, jsonify

import os
import pandas as pd
import fitz 
from docx import Document
import webview
import threading

app = Flask(__name__)

# ===============================================================
UPLOAD_FOLDER = r'C:\Users\Uporabnik\iCloudDrive\_Programming\.git\Tabloo\server\data'
ALLOWED_EXTENSIONS = {'xlsx', 'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ===============================================================
# search files
def search_files(query):
    results = []
    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        if filename.endswith(".xlsx"):
            try:
                df = pd.read_excel(filepath)
                for idx, row in df.iterrows():
                    if row.astype(str).str.contains(query, case=False).any():
                        results.append({
                            "file": filename,
                            "row_number": idx + 2,
                            "data": row.to_dict()
                        })
            except Exception as e:
                print(f"Error reading Excel: {filename} — {e}")

        elif filename.endswith(".pdf"):
            try:
                with fitz.open(filepath) as doc:
                    for page_num, page in enumerate(doc, 1):
                        text = page.get_text()
                        if query.lower() in text.lower():
                            snippet = text[:500].replace("\n", " ")
                            results.append({
                                "file": filename,
                                "row_number": f"PDF Page {page_num}",
                                "data": {"text": snippet}
                            })
            except Exception as e:
                print(f"Error reading PDF: {filename} — {e}")

        elif filename.endswith(".docx"):
            try:
                doc = Document(filepath)
                full_text = "\n".join([p.text for p in doc.paragraphs])
                if query.lower() in full_text.lower():
                    snippet = full_text[:500].replace("\n", " ")
                    results.append({
                        "file": filename,
                        "row_number": "Word Document",
                        "data": {"text": snippet}
                    })
            except Exception as e:
                print(f"Error reading DOCX: {filename} — {e}")

    return results

# ===============================================================
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# ===============================================================
# get searched text
@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    results = search_files(query)
    return jsonify(results)

# ===============================================================
# send found things
@app.route("/upload", methods=["POST"])
def upload_files():
    if 'files' not in request.files:
        return jsonify({"error": "No files part"}), 400
    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No files selected"}), 400

    for file in files:
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
        else:
            return jsonify({"error": f"Invalid file type for {file.filename}"}), 400
    return jsonify({"success": True})

# ===============================================================
def run_flask():
    app.run(debug=False, use_reloader=False)

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    # app.run(debug=True)

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    webview.create_window("QueriFlow", "http://127.0.0.1:5000", width=650, height=850)
    webview.start()
