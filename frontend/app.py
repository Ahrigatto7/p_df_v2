
import streamlit as st
from datetime import datetime
import requests

st.set_page_config(page_title="AI 문서 대시보드", layout="wide")

# 상태 체크
def check_backend():
    try:
        res = requests.get("http://localhost:8000/documents")
        if res.status_code == 200:
            return True, res.json()
        else:
            return False, {}
    except:
        return False, {}

# 헤더 및 상태
st.title("📚 AI 문서 관리 대시보드")
st.markdown(f"**접속 시각:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

status, data = check_backend()
if status:
    st.success("✅ 백엔드 서버 연결됨")
    if isinstance(data, list):
        doc_counts = {}
        for doc in data:
            dt = doc.get("doc_type", "기타")
            doc_counts[dt] = doc_counts.get(dt, 0) + 1
        st.subheader("📊 문서 통계 요약")
        for dtype, count in doc_counts.items():
            st.write(f"- **{dtype}**: {count}개")
else:
    st.error("❌ 백엔드 서버 연결 실패 - FastAPI가 실행 중인지 확인하세요.")

st.sidebar.title("📊 메뉴")
menu = st.sidebar.radio("이동", (
    "📥 문서 업로드/벡터화", 
    "💬 AI 검색(QA)", 
    "🧠 프롬프트 관리", 
    "📄 문서 관리", 
    "📜 CRUD/이력", 
    "🕸️ 관계 시각화"
))

if menu == "📥 문서 업로드/벡터화":
    try:
        from pages import vectorize_ui
        vectorize_ui.render()
    except Exception as e:
        st.error(f"vectorize_ui 오류: {e}")

elif menu == "💬 AI 검색(QA)":
    try:
        from pages import search_ui
        search_ui.render()
    except Exception as e:
        st.error(f"search_ui 오류: {e}")

elif menu == "🧠 프롬프트 관리":
    try:
        from pages import prompt_template_ui
        prompt_template_ui.render()
    except Exception as e:
        st.error(f"prompt_template_ui 오류: {e}")

elif menu == "📄 문서 관리":
    try:
        from pages import document_ui
        document_ui.render()
    except Exception as e:
        st.error(f"document_ui 오류: {e}")

elif menu == "📜 CRUD/이력":
    try:
        from pages import history_log_ui
        history_log_ui.render()
    except Exception as e:
        st.error(f"history_log_ui 오류: {e}")

elif menu == "🕸️ 관계 시각화":
    try:
        from pages import visualize_ui
        visualize_ui.render()
    except Exception as e:
        st.error(f"visualize_ui 오류: {e}")
