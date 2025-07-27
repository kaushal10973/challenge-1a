# Challenge 1A - PDF Outline Extractor

## 🔍 About

Extracts a structured outline (Title, H1, H2, H3) from PDFs and outputs JSON.

## 🧠 Features

- Accepts PDF files (≤ 50 pages)
- Extracts title + headings with level and page number
- Runs offline in Docker (no internet required)
- Docker-compatible with `linux/amd64` (CPU-only)

## 📂 Folder Structure

- `input/`  → place PDFs here
- `output/` → generated JSONs
- `app/`    → contains `main.py` and dependencies

## 🛠 How to Build and Run (Offline)

```bash
docker build --platform linux/amd64 -t challenge-1a:dev .

# Windows PowerShell
docker run --rm -v "${PWD}/input:/app/input" -v "${PWD}/output:/app/output" --network none challenge-1a:dev

# OR Windows CMD
docker run --rm -v "%cd%\input:/app/input" -v "%cd%\output:/app/output" --network none challenge-1a:dev
