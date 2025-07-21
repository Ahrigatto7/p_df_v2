# AI 문서 QA 시스템

이 저장소는 FastAPI 백엔드와 Streamlit 프론트엔드로 구성된 문서 검색 및 관리 서비스 예제입니다.

## 실행 방법
1. 필요한 파이썬 패키지를 설치합니다.
   ```bash
   pip install -r requirements.txt
   ```
2. 프로젝트 루트에 `.env` 파일을 생성하고 다음 환경 변수를 설정합니다.
   ```env
   OPENAI_API_KEY=your-openai-key
   DB_URL=postgresql://user:pass@host:port/dbname  # 선택 사항, 기본은 SQLite
   ```
3. 백엔드와 프론트엔드를 실행합니다.

## 환경 변수
- **OPENAI_API_KEY**: LLM 호출을 위해 필수로 설정해야 합니다.
- **DB_URL**: 데이터베이스 연결 URL. 설정하지 않으면 `p_df_main.db` SQLite 파일을 사용합니다.

`.env` 파일은 민감한 정보를 포함하므로 저장소에 커밋하지 않도록 `.gitignore`에 추가되어 있습니다.
