
# 📘 AI 기반 문서 QA 시스템 아키텍처 문서

본 문서는 FastAPI + Streamlit 기반의 통합 문서 검색 및 관리 시스템의 아키텍처를 설명합니다.

---

## 🗂️ 시스템 구성 개요

```
사용자
  │
  ▼
📊 Streamlit (app.py)
  ├─ 📥 문서 업로드 (vectorize_ui.py)
  ├─ 🔍 검색/질의응답 (search_ui.py)
  ├─ 📄 문서 관리 (document_ui.py)
  └─ 🧠 프롬프트 관리 (prompt_template_ui.py)
      │
      ▼
🚀 FastAPI (api_router.py)
  ├─ 📚 벡터화 엔진 (vector_ops.py)
  ├─ 📄 PDF 텍스트 추출 (pdf_utils.py)
  ├─ 🧠 LLM 호출기 (llm_runner.py)
  └─ 🐘 데이터베이스 연동 (models.py, crud.py)
      │
      ▼
📦 PostgreSQL
```

---

## 📦 주요 기능별 구성

### 1. 문서 업로드 및 벡터화
- Streamlit: `vectorize_ui.py`
- API: `POST /vectorize`
- 벡터화 로직: `vector_ops.vectorize_file()`
- DB 저장: `crud.save_document()` 사용

### 2. 질의응답 (Search)
- Streamlit: `search_ui.py`
- API: `POST /search`
- 벡터 검색: `hybrid_search()`
- 답변 생성: `llm_runner.run_prompt_template()`

### 3. 문서 관리
- Streamlit: `document_ui.py`
- API: `GET /documents`
- DB 조회: `crud.get_all_documents()`

### 4. 프롬프트 템플릿 관리
- Streamlit: `prompt_template_ui.py`
- API:
  - `GET /prompt_templates`
  - `GET /prompt_template`
  - `PUT /prompt_template`
- 파일 기반 템플릿 관리

---

## ⚙️ 백엔드 기술스택

| 구성 요소 | 설명 |
|-----------|------|
| FastAPI | REST API 제공 |
| LangChain | 문서 임베딩 및 검색 |
| PostgreSQL | 문서 메타/히스토리 저장 |
| OpenAI | LLM 응답 생성 |
| PyPDF2 | PDF 텍스트 추출 |

---

## ✅ 실행 방법 (로컬)

```bash
# 백엔드 실행
uvicorn backend.api_router:app --reload

# 프론트 실행
streamlit run frontend/app.py

# 통합 실행 (Windows)
run_all.bat
```

---

## 📁 디렉토리 구조 요약

```
📁 backend/
    ├─ api_router.py
    ├─ crud.py
    ├─ db.py / db_init.py
    ├─ models.py
    ├─ pdf_utils.py
    ├─ vector_ops.py
    ├─ llm_runner.py

📁 frontend/pages/
    ├─ vectorize_ui.py
    ├─ search_ui.py
    ├─ prompt_template_ui.py
    ├─ document_ui.py
    ├─ history_log_ui.py

📄 frontend/app.py
```

---
