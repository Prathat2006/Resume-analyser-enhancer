# AI Resume Analyzer & Enhancer

A powerful AI-driven system that analyzes resumes, matches them against job descriptions, enhances them with AI suggestions, and scores compatibility. Built with **FastAPI**, **LangChain**, **LLM providers (Groq, OpenRouter, Ollama, LM Studio)**, and a modern **React + Streamlit frontend**.

---

## 🚀 Features

* 📄 Upload resume PDFs for parsing & enhancement.
* 🤖 Dynamic use of multiple LLM providers (Groq, OpenRouter, Ollama, LM Studio).
* 📝 Job description parsing (via web scraping or manual input).
* 📊 Compatibility scoring using embeddings & similarity models.
* ⚡ Mode switching (default, fast, offline) via `config.ini`.
* 🔗 Frontend integration for interactive analysis.

---

## 📂 Project Structure

```
├── backend/              # FastAPI backend
│   ├── main.py           # Entry point
│   ├── pdf_parser.py     # Resume parsing
│   ├── enhancer.py       # Resume enhancement
│   ├── scorer.py         # Scoring logic
│   └── config.ini        # Configuration file
├── frontend/             # React + Streamlit frontend
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## ⚙️ Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Install PyTorch (Required for embeddings)
 will increased speed if used cuda version  of torch (nvidia-gpu-only)
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 4. Frontend Setup

Frontend is available here 👉 [Frontend Link](https://github.com/Prathat2006/Resume-analyser-enhancer-frontend.git)

```bash
cd frontend
npm install
npm run dev
```

---

## 🔑 API Keys & Providers Setup

### 1. **Groq API**

* Get an API key from [Groq Console](https://console.groq.com/).
* Add it to your environment:

```bash
export GROQ_API_KEY="your_api_key_here"
```

### 2. **OpenRouter API**

* Sign up at [OpenRouter](https://openrouter.ai/).
* Generate API key and set:

```bash
export OPENROUTER_API_KEY="your_api_key_here"
```

### 3. **Ollama Setup**

* Install Ollama: [Download Ollama](https://ollama.ai/).
* Pull a model (example: Qwen3):

```bash
ollama pull qwen3:4b
```

### 4. **LM Studio Setup**

* Install LM Studio: [Download LM Studio](https://lmstudio.ai/).
* Start a local API server from LM Studio settings.
* Ensure it runs at `http://localhost:1234` (configurable).

---

## ⚡ Configuration (Mode Switching)

The project supports **3 modes**: `default`, `fast`, `offline`.

Edit **`config.ini`**:

```ini
[llms]
source = groq
model = meta-llama/llama-4-scout-17b-16e-instruct
temperature = 0.0

[llms_openrouter]
source = openrouter
model = deepseek/deepseek-r1:free
temperature = 0.9
site_url = http://localhost
site_name = MyApp

[llms_groq]
source = groq
model = moonshotai/kimi-k2-instruct
temperature = 0.0

[llms_ollama]
source = ollama
model = qwen3:4b
temperature = 0.0

[llms_lmstudio]
source = lmstudio
model = qwen/qwen3-4b-2507
temperature = 0.0

[embedding_model]
embedding_model = Qwen/Qwen3-Embedding-0.6B

[SIM_THRESHOLD]
skill_words_strictness = 0.8

[offline-order]
order = lmstudio, ollama

[fast-order]
order = groq, openrouter

[default-order]
order = groq, lmstudio, ollama, openrouter

[mode]
order = default
```

To switch mode, update:

```ini
[mode]
order = fast
```

---

## ▶️ Running the App

### Backend

```bash
cd backend
uvicorn server:app --reload
```

### Frontend

```bash
cd frontend
npm run dev
```

or 
if frontend is not cloned```bash
streamlit run ui/streamlitui.py
```

---

## 📊 Workflow

1. User uploads resume (PDF).
2. Backend extracts text → LLM parses structure.
3. Job description fetched (manual / web scraping).
4. Embedding models compute similarity score.
5. Enhanced resume generated + scored.
6. Frontend displays resume + score + suggestions.

---

## 🛠️ Tech Stack

* **Backend**: FastAPI, LangChain, Transformers
* **Frontend**: React, Streamlit
* **LLMs**: Groq, OpenRouter, Ollama, LM Studio
* **Embeddings**: Qwen/Qwen3-Embedding-0.6B
* **PDF Parsing**: PyMuPDF, ReportLab

---

## 🎯 Roadmap

* [ ] Add Docker support
* [ ] One-click mode switch via CLI
* [ ] Save and compare multiple resumes
* [ ] Generate tailored resumes per job post

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## 📜 License

MIT License © 2025 Your Name
