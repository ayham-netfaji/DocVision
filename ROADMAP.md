# DocVision — Roadmap

> Distilled from [DocVision_Project_Report.md](file:///c:/Users/HP/OneDrive/Desktop/vs%20code/ocr%20project/DocVision_Project_Report.md)
> **Rule: No phase starts until previous phase passes its test gate.**

---

## Phase 0 — Architecture & Planning ✅ (this file)
- [x] Analyze report
- [x] Create ROADMAP.md
- [x] Create CHECKPOINT.md
- **Gate:** Files exist, plan reviewed

---

## Phase 1 — Project Setup ✅
- [x] Init Git repo + `.gitignore`
- [x] Create `backend/` with Python venv, FastAPI, Uvicorn
- [x] Create `frontend/` with Vite + React + TypeScript
- [x] Verify both servers start (health endpoint + dev page)
- **Gate:** ✅ `GET /api/v1/health` returns `{"status":"ok"}`, React dev page returns 200

---

## Phase 2 — Frontend Foundation
- [ ] Tailwind CSS setup
- [ ] React Router (Home, Scanner, Result, History pages)
- [ ] Navbar component
- [ ] Home page with upload zone (drag & drop + file picker)
- [ ] JPG/PNG/WEBP validation client-side
- **Gate:** Navigate all routes, upload zone accepts valid images, rejects others

---

## Phase 3 — Backend Foundation
- [ ] FastAPI project structure (`api/routes/`, `services/`, `schemas/`, `core/`, `utils/`)
- [ ] Pydantic schemas for document & OCR response
- [ ] CORS config
- [ ] File upload endpoint `POST /api/v1/documents/scan` (accept image, return stub)
- [ ] File validation (type, size)
- [ ] Temp file cleanup
- **Gate:** Upload image via curl/Postman, get stub JSON back, invalid files rejected

---

## Phase 4 — Image Upload Integration
- [ ] Connect frontend upload zone to backend endpoint via Axios
- [ ] Show image preview after upload
- [ ] Scanner page with "Scan Document" button
- [ ] Processing status UI (step indicators + progress bar)
- **Gate:** Upload from browser, see preview, click scan, see processing indicators

---

## Phase 5 — CV Pipeline Core (OpenCV)
- [ ] `document_processor.py` — resize, grayscale, Gaussian blur
- [ ] Unit test: feed sample image, verify output dimensions & channels
- **Gate:** Pytest passes for resize + grayscale + blur

---

## Phase 6 — Document Detection
- [ ] `edge_detector.py` — Canny edge detection + contour detection
- [ ] Find largest 4-sided contour = document boundary
- [ ] Fallback: if no 4-point contour found, use full image
- [ ] Unit test: detect known document in test image
- **Gate:** Pytest passes, document corners identified correctly

---

## Phase 7 — Perspective Correction
- [ ] `perspective.py` — four-corner ordering + `cv2.getPerspectiveTransform` + `cv2.warpPerspective`
- [ ] Unit test: tilted document becomes rectangular
- **Gate:** Pytest passes, output image is rectangular crop

---

## Phase 8 — Image Enhancement
- [ ] `image_enhancer.py` — contrast, brightness, sharpening, adaptive threshold, CLAHE
- [ ] Multiple enhancement presets (scan, photo, low-light)
- [ ] Unit test: enhanced image has better contrast metrics than input
- **Gate:** Pytest passes, visual inspection of enhanced output

---

## Phase 9 — OCR Integration
- [ ] Install Tesseract OCR system binary
- [ ] `ocr_service.py` — PyTesseract wrapper, confidence extraction
- [ ] Wire full pipeline: upload → process → detect → correct → enhance → OCR → return text + confidence
- [ ] Unit test: OCR on clean test doc produces expected text
- **Gate:** Pytest passes, `POST /api/v1/documents/scan` returns real extracted text

---

## Phase 10 — Result UI
- [ ] Result page: side-by-side processed image + extracted text
- [ ] OCR confidence display
- [ ] Copy text button
- [ ] Download TXT button
- [ ] "Show Processing" demo view (all CV stages displayed)
- **Gate:** Full end-to-end: upload → scan → see result with text, copy/download work

---

## Phase 11 — Export
- [ ] Download PDF (use ReportLab or simple HTML-to-PDF)
- **Gate:** PDF downloads with extracted text

---

## Phase 12 — Database & History
- [ ] PostgreSQL + SQLAlchemy + Alembic setup
- [ ] `documents` and `ocr_results` tables
- [ ] `GET /api/v1/documents/{id}`, `DELETE /api/v1/documents/{id}`
- [ ] History page in frontend
- **Gate:** Scan, see in history, retrieve, delete

---

## Phase 13 — Testing & Quality
- [ ] Backend: Pytest suite covering all services + endpoints
- [ ] Frontend: Vitest + React Testing Library for key components
- [ ] Ruff (Python), ESLint + Prettier (frontend)
- [ ] OCR performance evaluation (CER/WER comparison: raw vs processed)
- **Gate:** All tests pass, linters clean, performance report generated

---

## Phase 14 — Docker
- [ ] Dockerfile for backend (with Tesseract)
- [ ] Dockerfile for frontend
- [ ] docker-compose.yml (frontend + backend + PostgreSQL)
- **Gate:** `docker compose up` runs full app

---

## Phase 15 — CI/CD & Deployment
- [ ] GitHub Actions: lint → test → build
- [ ] Deploy to cloud
- **Gate:** Push triggers pipeline, app accessible online

---

## Future Phases (post-core)

| Phase | Feature |
|-------|---------|
| 16 | AI: Summarization, OCR Correction, Classification |
| 17 | AI: Q&A, Structured Extraction, Translation |
| 18 | RAG: pgvector + embeddings + multi-doc search |
| 19 | Mobile: React Native + Expo |

---

> **Core principle from report:** *Do not add complexity until the previous layer is stable and tested.*
