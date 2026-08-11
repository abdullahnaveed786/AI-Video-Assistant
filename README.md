# AI Video Assistant

A compact tool to transcribe, summarise, and chat with meeting-style videos (YouTube or local files). Designed for quick experimentation with local Whisper + Mistral LLMs and a Chroma-powered RAG chat.

## Quick Features
- Transcribe audio: local Whisper (English) or Sarvam (Hinglish)
- Generate title and concise meeting summary (Mistral)
- Extract action items, decisions, open questions
- Build a Chroma vector index and provide RAG chat
- Streamlit UI and a simple CLI


## Quickstart

1. Clone the repo:

```bash
git clone https://github.com/abdullahnaveed786/AI-Video-Assistant.git
cd AI-Video-Assistant
```

2. Create and activate a virtual environment, then install deps:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r Requirements.txt
```

3. Run the app (Streamlit UI) or CLI:

```bash
streamlit run app.py
# or
python main.py
```
