# 🎬 AI Video Assistant — Meeting Intelligence & RAG Chat

[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/Framework-LangChain-1C3C3C?style=flat-square)](https://www.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/VectorStore-ChromaDB-FF6F61?style=flat-square)](https://www.trychroma.com/)
[![Whisper](https://img.shields.io/badge/STT-OpenAI_Whisper-lightgrey?style=flat-square&logo=openai)](https://github.com/openai/whisper)
[![Mistral](https://img.shields.io/badge/LLM-Mistral_AI-orange?style=flat-square)](https://mistral.ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

**AI Video Assistant** is an intelligent, single-stack meeting intelligence application that transcribes, summarizes, and provides a context-bounded Q&A chat for video and audio content. Built with **Streamlit**, **LangChain**, **ChromaDB**, **OpenAI Whisper (Local)**, and **Mistral AI**, it processes both YouTube links and local media files into executive summaries, action items, key decisions, and an interactive RAG (Retrieval-Augmented Generation) chat session.

---

## ✨ Features

- 🎥 **Dual Media Processing**: Accepts any YouTube URL or local audio/video file path.
- 🎙️ **Multi-Language Speech-to-Text (STT)**:
  - **English**: Local transcription using **OpenAI Whisper** (runs on CPU/GPU; defaults to `tiny` for speed).
  - **Hinglish**: Hybrid transcription and translation via the **Sarvam AI STT** API (`saaras:v2.5`).
- 📋 **Meeting Summaries & Insights**: Extract structured intelligence from transcripts:
  - Executive meeting summaries
  - Action items & assignments
  - Key decisions made
  - Unresolved or open questions
- 🧠 **Context-Bounded Vector RAG**: Creates local document splits, embeds them using HuggingFace (`all-MiniLM-L6-v2`), indexes them in **ChromaDB**, and provides an interactive chatbot context-bounded to the meeting transcript.
- 🎨 **Glassmorphism Dark Theme UI**: A custom high-density Streamlit UI featuring:
  - An animated grid background and glass-style cards.
  - A live sidebar-integrated pipeline step tracker (Audio → Transcription → Summarization → RAG).
  - Clean collapsible transcript viewing and a unified Q&A conversation panel.

---

## 🏗️ Architecture Pipeline

```
  ┌─────────────────────────────────────────────────────────────┐
  │                   Media Source Input                        │
  │              (YouTube URL or Local File)                    │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                        utils/                               │
  │         yt-dlp + ffmpeg Audio Extraction & Conversion       │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌──────────────────────────────┴──────────────────────────────┐
  │                        core/                                │
  │  Whisper STT (English)  │  Sarvam AI Translation (Hinglish)  │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                 Mistral AI Map-Reduce Engine                │
  │  Summary  │  Action Items  │  Key Decisions  │  Questions   │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │               ChromaDB Vector RAG Engine                    │
  │     HuggingFace Embeddings + LangChain LCEL RAG Chain       │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │               Streamlit Interactive Web UI                  │
  │          Transcribe, Analyze & Chat with Meetings           │
  └─────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Directory Structure

```
AI-Video-Assistant/
├── core/
│   ├── extractor.py       # Actions, Decisions, and Open Questions extraction
│   ├── rag_engine.py      # LangChain + Mistral Q&A chain
│   ├── summarizer.py      # Map-Reduce summary & Title generation
│   ├── transcriber.py     # Local Whisper & Sarvam AI STT
│   └── vector_store.py   # ChromaDB vector index builder
├── utils/
│   └── audio_processor.py # yt-dlp, wave chunking, and ffmpeg WAV converter
├── .env                  # Project API keys and configuration
├── app.py                # Streamlit Web UI Entrypoint
├── main.py               # Command Line Interface (CLI) Entrypoint
├── test.py               # Offline/test pipeline script
└── Requirements.txt      # Python dependencies
```

---

## 🚀 Local Installation & Setup Guide

### 1. Prerequisites
- **Python**: `>=3.10` (Python 3.12+ recommended)
- **System Dependency**: `ffmpeg` (must be installed and added to your system `PATH`)
- **Package Manager**: `uv` (recommended for ultra-fast installs) or `pip`

### 2. Environment Configuration
Create a `.env` file in the root directory:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
SARVAM_API_KEY=your_sarvam_api_key_here
WHISPER_MODEL=tiny       # Options: tiny, base, small, medium, large
```

### 3. Install Dependencies

Using `uv` (recommended):
```bash
# Create virtual environment and install packages
uv venv
uv pip install -r Requirements.txt
```

Using standard `pip`:
```bash
# Create virtual environment
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

# Install requirements
pip install -r Requirements.txt
```

---

## 💻 Running the Application

### Launch the Streamlit Web UI (Recommended)
This launches the custom dark-themed browser interface:
```bash
# Activate your virtual environment first if not active
streamlit run app.py
```
The application will run at **`http://localhost:8501`**.

### Launch the Command Line Interface (CLI)
You can run the pipeline directly inside your terminal:
```bash
python main.py
```

---

## 🛠️ Troubleshooting & Advanced Notes

### 1. YouTube Downloads Fail (HTTP 403 Forbidden)
`yt-dlp` requests may occasionally be flagged or throttled by YouTube. The application includes a custom configuration to bypass this:
- We automatically impersonate mobile/browser clients (using `extractor_args` in [`utils/audio_processor.py`](utils/audio_processor.py)).
- If you still encounter issues, try updating your package:
  ```bash
  uv pip install -U yt-dlp
  ```

### 2. Python 3.13+ Compatibility (`audioop` error)
Python 3.13 and 3.14 removed the deprecated standard library module `audioop` (PEP 594). 
- If you run the project on Python 3.13+, the package manager will install the `audioop-lts` backport automatically so `pydub` continues to compile and slice audio seamlessly.

### 3. Slow Local Transcription
By default, the project runs on CPU.
- We have set `WHISPER_MODEL=tiny` in `.env` to ensure fast processing on normal processors.
- If you have an NVIDIA GPU, make sure you install PyTorch with CUDA support to dramatically accelerate Whisper `small` or `medium` models:
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
  ```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.
