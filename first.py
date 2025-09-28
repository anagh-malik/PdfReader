from flask import Flask, render_template, request, Response
import json
import PyPDF2
import requests

app = Flask(__name__)

# Store uploaded PDFs in memory
uploaded_pdfs = {}

# Map frontend model IDs to Ollama model names
OLLAMA_MODELS = {
    "llama-3.1": "llama3.1",
    "mistral": "mistral",
    "gpt-oss": "gpt-oss",
    "gemma-2": "gemma2",
}

def call_ollama_model(question, model, pdf_text=""):
    """
    Calls the Ollama model via HTTP API and streams the output.
    """
    if pdf_text:
        prompt = f"{pdf_text[:2000]}\n\nQuestion: {question}"
    else:
        prompt = question

    model_name = OLLAMA_MODELS.get(model, "gpt-oss")
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": True  # Enable streaming
    }
    try:
        with requests.post(url, json=payload, stream=True, timeout=120) as response:
            response.raise_for_status()
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        data = json.loads(line)
                        text = data.get("response", "")
                        yield f"data: {json.dumps({'text': text})}\n\n"
                    except Exception as e:
                        yield f"data: {json.dumps({'text': '⚠️ Error: ' + str(e)})}\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'text': '⚠️ Error: ' + str(e)})}\n\n"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    model = data.get("model", "gpt-oss")
    pdf_name = data.get("pdf_name")

    pdf_text = ""
    if pdf_name and pdf_name in uploaded_pdfs:
        pdf_text = uploaded_pdfs[pdf_name]

    def stream():
        for chunk in call_ollama_model(question, model, pdf_text):
            yield chunk

    return Response(stream(), mimetype="text/event-stream")

@app.route("/")
def index():
    return render_template("index.html")  # HTML with embedded JS/CSS

@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    """
    Receives PDF file, extracts text, and stores in memory.
    """
    file = request.files.get("pdf")
    if not file:
        return {"status": "error", "message": "No file uploaded"}, 400

    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        uploaded_pdfs[file.filename] = text
        return {"status": "success", "message": f"Processed {file.filename}", "pdf_name": file.filename}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")