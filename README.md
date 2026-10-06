# DocVision: Computer Vision Document Scanner & OCR System

![DocVision CI](https://github.com/docvision/docvision/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.14-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.10+-5C3EE8.svg)
![React](https://img.shields.io/badge/React-19-61DAFB.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178C6.svg)
![Vite](https://img.shields.io/badge/Vite-8+-646CFF.svg)
![TailwindCSS](https://img.shields.io/badge/Tailwind-v4-38B2AC.svg)

**DocVision** is a document scanner and optical character recognition (OCR) application that transforms angled, poorly-lit mobile camera photos of documents into perspective-corrected, binarized, and searchable digital text and formatted PDF reports.

---

## 🌟 Key Features

1. **5-Stage Computer Vision Pipeline:**
   - **Stage 1 (Grayscale & Downscaling):** Aspect-ratio preserving downsampling and luminance normalization.
   - **Stage 2 (Gaussian Filtering & Canny Edge Detection):** Auto-Canny thresholding based on median image intensity.
   - **Stage 3 (Contour Approximation & 4-Corner Detection):** Morphological closing, perimeter contour approximation (`approxPolyDP`), and clockwise vertex ordering.
   - **Stage 4 (Homography Perspective Rectification):** 4-point perspective warp (`cv2.warpPerspective`) restoring top-down view.
   - **Stage 5 (Image Enhancement & Binarization):** Local contrast equalization (CLAHE), unsharp masking, and adaptive Gaussian thresholding.
2. **High-Accuracy OCR Text Extraction:**
   - Word-level confidence estimation, character & word counters.
   - Fallback error resilience for local Tesseract binaries.
3. **Academic CV Showcase:**
   - Interactive UI toggle decomposing all 5 CV pipeline steps side-by-side with explanations.
4. **Professional Export:**
   - Download structured PDF reports with confidence badges, scan thumbnails, and formatted text via ReportLab.
   - One-click TXT download and clipboard copying.
5. **Database Persistence & Scan History:**
   - SQLite (default) and PostgreSQL support with SQLAlchemy.
   - Searchable history table, scan thumbnail previews, and instant reload.
6. **AI Document Summarization:**
   - Integrated OpenRouter API (Nvidia Nemotron model) for intelligent document summaries and classification.
7. **Docker & CI/CD Ready:**
   - Multi-stage Docker build with Nginx reverse proxy.
   - Complete GitHub Actions CI pipeline running linters, tests, and container builds.

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- Node.js 20+
- Tesseract OCR (`tesseract` on PATH)

### 1. Backend Setup
```bash
cd backend
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Configure Environment
echo "OPENROUTER_API_KEY=your_key_here" > .env

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Backend runs at `http://127.0.0.1:8000` (API Docs: `http://127.0.0.1:8000/docs`).

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at `http://localhost:5173`.

---

## 🐳 Quick Start (Docker Compose)

Run the entire stack (PostgreSQL + FastAPI + React/Nginx) with one command:

```bash
docker compose up --build
```

- **Frontend Application:** `http://localhost:3000`
- **Backend API & Swagger Docs:** `http://localhost:8000/docs`
- **PostgreSQL Database:** `localhost:5432`

---

## 🧪 Testing & Quality Gates

### Backend Tests & Linting
```bash
cd backend
# Run all 29 pytest assertions
pytest -v

# Run Ruff linter
ruff check app tests
```

### Frontend Tests & Linting
```bash
cd frontend
# Run Vitest component tests (6 passed)
npm run test

# Run Oxlint
npm run lint

# Production build verification
npm run build
```

---

## 📡 API Endpoints Summary

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/health` | Service health status |
| `POST` | `/api/v1/documents/scan` | Upload image, run 5-stage CV + OCR, persist scan |
| `GET` | `/api/v1/documents` | List scanned documents with pagination |
| `GET` | `/api/v1/documents/{id}` | Retrieve specific document scan and stages |
| `DELETE` | `/api/v1/documents/{id}` | Delete document and associated OCR results |
| `GET` | `/api/v1/export/{id}/pdf` | Stream formatted PDF document report |
| `POST` | `/api/v1/ai/summarize` | Generate AI summary for extracted text using OpenRouter |

---

## 📄 License
MIT
