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

## Phase 2 — Frontend Foundation ✅
- [x] Tailwind CSS setup
- [x] React Router (Home, Scanner, Result, History pages)
- [x] Navbar component
- [x] Home page with upload zone (drag & drop + file picker)
- [x] JPG/PNG/WEBP validation client-side
- **Gate:** ✅ TypeScript build clean, dev server returns 200, route navigation active

---

## Phase 3 — Backend Foundation ✅
- [x] FastAPI project structure (`api/routes/`, `services/`, `schemas/`, `core/`, `utils/`)
- [x] Pydantic schemas for document & OCR response
- [x] CORS config
- [x] File upload endpoint `POST /api/v1/documents/scan` (accept image, return stub)
- [x] File validation (type, size)
- [x] Temp file cleanup
- **Gate:** ✅ Pytest passes all 4 tests (health, OCR status, upload validation, format checking)

---

## Phase 4 — Image Upload Integration ✅
- [x] Connect frontend upload zone to backend endpoint via Axios
- [x] Show image preview after upload
- [x] Scanner page with "Scan Document" button
- [x] Processing status UI (step indicators + progress bar)
- **Gate:** ✅ TypeScript build clean, full E2E flow (upload -> progress simulation -> live scan response -> results)

---

## Phase 5 — CV Pipeline Core (OpenCV) ✅
- [x] `document_processor.py` — resize, grayscale, Gaussian blur
- [x] Unit test: feed sample image, verify output dimensions & channels
- **Gate:** ✅ Pytest passes 9/9 tests for resize + grayscale + blur + API integration

---

## Phase 6 — Document Detection ✅
- [x] `edge_detector.py` — Canny edge detection + contour detection
- [x] Find largest 4-sided contour = document boundary
- [x] Fallback: if no 4-point contour found, use full image
- [x] Unit test: detect known document in test image
- **Gate:** ✅ Pytest passes 12/12 tests, document corners identified correctly, fallback tested

---

## Phase 7 — Perspective Correction ✅
- [x] `perspective.py` — four-corner ordering + `cv2.getPerspectiveTransform` + `cv2.warpPerspective`
- [x] Unit test: tilted document becomes rectangular
- **Gate:** ✅ Pytest passes 15/15 tests, output image is rectangular top-down crop, scaled to full resolution

---

## Phase 8 — Image Enhancement ✅
- [x] `image_enhancer.py` — contrast, brightness, sharpening, adaptive threshold, CLAHE
- [x] Multiple enhancement presets (scan_bw, enhanced_color, grayscale)
- [x] Unit test: enhanced image has better contrast metrics than input
- **Gate:** ✅ Pytest passes 19/19 tests, CLAHE contrast, Otsu, and adaptive binarization verified

---

## Phase 9 — OCR Integration ✅
- [x] Install Tesseract OCR / PyTesseract wrapper
- [x] `ocr_service.py` — PyTesseract wrapper, confidence extraction, automated binary resolution
- [x] Wire full pipeline: upload → process → detect → correct → enhance → OCR → return text + confidence
- [x] Unit test: OCR extraction interface and confidence parsing
- **Gate:** ✅ Pytest passes 22/22 tests, `POST /api/v1/documents/scan` runs full end-to-end CV + OCR pipeline

---

## Phase 10 — Result UI ✅
- [x] Result page: side-by-side processed image + extracted text
- [x] OCR confidence, word count & character count display
- [x] Copy text button
- [x] Download TXT button
- [x] "Show Processing" demo view (all CV stages decomposed: Grayscale, Canny, 4-Point Quad, Homography Warp, Enhanced B&W)
- [x] Text reader font size adjustment (S/M/L)
- **Gate:** ✅ Full end-to-end: upload → scan → see result with text, copy/download work, academic CV stages showcase verified

---

## Phase 11 — Export ✅
- [x] Download PDF service via ReportLab (`pdf_exporter.py`)
- [x] Streaming PDF endpoint `GET /api/v1/export/{id}/pdf`
- [x] Download PDF button in frontend `Result.tsx` toolbar
- [x] Download TXT button in frontend
- **Gate:** ✅ Pytest passes 25/25 tests, PDF downloads with formatted report, confidence header and embedded scan image

---

## Phase 12 — Database & History ✅
- [x] Database models via SQLAlchemy (`Document`, `OCRResult` with cascade delete)
- [x] Session management & CRUD operations (`db/crud.py`, `db/session.py`)
- [x] Document listing, fetching, and deletion REST endpoints: `GET /api/v1/documents`, `GET /api/v1/documents/{id}`, `DELETE /api/v1/documents/{id}`
- [x] Interactive History page in frontend with keyword search, confidence badges, scan thumbnails, and delete actions
- **Gate:** ✅ Pytest passes 26/26 tests, full DB persistence lifecycle: scan saves to DB, displays in History, opens in Result, deletes cleanly

---

## Phase 13 — Testing & Quality ✅
- [x] Backend: Pytest suite covering all services + endpoints (29 tests passing)
- [x] Frontend: Vitest + React Testing Library for key components (`UploadZone`, `ProcessingStatus` passing 6 tests)
- [x] Ruff (Python with custom pyproject.toml) and Oxlint (frontend) completely clean
- [x] OCR performance evaluation service (`ocr_evaluator.py` with CER, WER, and accuracy gain metrics)
- **Gate:** ✅ All tests pass (29 backend pytest, 6 frontend vitest), linters clean, OCR evaluation verified

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
