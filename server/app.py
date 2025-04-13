from flask import Flask, request, render_template, jsonify
import os
import pandas as pd

app = Flask(__name__)

UPLOAD_FOLDER = r'C:\Users\Uporabnik\iCloudDrive\_Programming\.git\Tabloo\server\data'
ALLOWED_EXTENSIONS = {'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Search Excel files
def search_excel_files(query):
    results = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith(".xlsx"):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            df = pd.read_excel(filepath)
            for idx, row in df.iterrows():
                if row.astype(str).str.contains(query, case=False).any():
                    results.append({
                        "file": filename,
                        "row_number": idx + 2,
                        "data": row.to_dict()
                    })
    return results

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    results = search_excel_files(query)
    return jsonify(results)

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

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
