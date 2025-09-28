# PDF Reader Chat with Ollama LLMs

This project lets you **chat with your PDF documents** using local Large Language Models (LLMs) served by [Ollama](https://ollama.com/). Upload a PDF, select an AI model (Llama 3.1, Mistral, GPT-OSS, or Gemma 2), and ask questions about the document in a chat interface. Answers are streamed live and rendered as Markdown for a rich, interactive experience—all on your own machine.

---

## Features

- **Upload any PDF** and extract its text for context-aware Q&A.
- **Choose from multiple open-source LLMs** (Llama 3.1, Mistral, GPT-OSS, Gemma 2).
- **Chat interface**: Ask questions and get answers about your PDF.
- **Streaming responses**: See the answer appear live as the model generates it.
- **Markdown rendering**: Answers support formatting, code, and lists.
- **Dark mode**: User-friendly interface with light/dark theme toggle.
- **Privacy-first**: All processing is local—your data never leaves your computer.

---

## How It Works

1. **Frontend** (`templates/index.html`):

   - Lets you select a model, upload a PDF, and chat.
   - Sends your question and selected model to the backend.
   - Streams and renders the model’s answer as Markdown.

2. **Backend** (`first.py`):

   - Flask server handles file uploads, chat requests, and serves the frontend.
   - Extracts text from uploaded PDFs using PyPDF2.
   - For each question, sends a prompt (with PDF context) to the selected Ollama model via its HTTP API.
   - Streams the model’s response back to the frontend using Server-Sent Events (SSE).

3. **Ollama**:
   - Runs locally and serves LLMs via an HTTP API.
   - Handles the actual language model inference.

---

## Getting Started (Local Use Only)

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com/) installed and running (`ollama serve`)
- Models downloaded in Ollama (e.g., `ollama pull mistral`)
- Install Python dependencies:
  ```sh
  pip install flask PyPDF2 requests
  ```

### Running the App

1. **Start Ollama server** (in one terminal):

   ```sh
   ollama serve
   ```

2. **Start Flask backend** (in your project directory):

   ```sh
   python PDF_Reader_Chat/first.py
   ```

3. **Open your browser** to [http://localhost:5000](http://localhost:5000)

---

## Why Is This Helpful?

- **Research**: Quickly extract insights from academic papers, reports, or e-books.
- **Productivity**: Summarize, search, or analyze large documents without manual reading.
- **Privacy**: All data stays on your machine—no cloud uploads.
- **Flexibility**: Choose the LLM that best fits your needs and hardware.

---

## File Structure

```
PDF_Reader_Chat/
├── first.py                # Flask backend
└── templates/
    └── index.html          # Frontend UI
```

---

## Security & Privacy

- All PDF and chat data is processed locally.
- No data is sent to third-party servers.

---

## Credits

- **Frontend**: Deepseek, Copilot
- **Backend**: ChatGPT, Copilot
- **Models**: Ollama open-source LLMs

---

**Enjoy chatting with your PDFs using local AI!**

