# YouTube Tools Backend

**FastAPI-based backend** for extracting YouTube video tags and metadata.

---

## ✨ Features

- Extract **all tags** from any YouTube video
- Full validation of YouTube URLs (including `youtu.be` short links)
- Strict 11-character video ID validation
- Clean, well-structured FastAPI architecture
- Professional error handling with custom messages
- Ready for production deployment (EC2, Railway, Render, etc.)
- Full type hints and Pydantic models

---

## 🛠 Tech Stack

- **Framework**: FastAPI
- **Validation**: Pydantic v2
- **YouTube Parsing**: yt-dlp
- **Linter & Formatter**: Ruff
- **Type Checking**: MyPy
- **ASGI Server**: Uvicorn + Gunicorn (production)

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/YT_BACKEND_TOOLS.git
cd YT_BACKEND_TOOLS