import streamlit as st
import subprocess
import time
import os
from custom_pages import dashboard_ui

# ---- 모던 스타일 사이드바 꾸미기 ----
st.set_page_config(page_title="AI 데이터 플랫폼", layout="wide")
st.markdown("""
    <style>
    /* 모던한 사이드바 타이틀 */
    .sidebar-title {font-size: 26px; font-weight: 700; color: #3D5AFE; margin-bottom: 10px;}
    .sidebar-section {font-size:15px; color:#555; margin-top:18px;}
    /* 라디오 버튼 사이 여백 */
    .sidebar-radio .stRadio > div { gap: 10px; }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-title">🧊 DATA MODERN</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-section">메뉴</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")

def start_backend_if_needed():
    if "STREAMLIT_CLOUD" in os.environ:
        return
    try:
        subprocess.Popen(
            ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(1)
    except Exception as e:
        print(f"❌ 백엔드 실행 실패: {e}")

start_backend_if_needed()

menu = st.sidebar.radio(
    "",
    (
        "🏠 대시보드",
        "📥 데이터 업로드/스키마",
        "📄 문서 벡터화",
        "🔍 통합 검색(QA/RAG)",
        "💬 프롬프트 관리",
        "🔗 데이터 병합/비교",
        "📊 관계/통계 시각화",
        "🕑 이력 관리",
        "⚙️ 사용자 설정",
    ),
    key="mainmenu"
)

if menu == "🏠 대시보드":
    from pages import dashboard_ui
    dashboard_ui.render()
elif menu == "📥 데이터 업로드/스키마":
    from pages import schema_ui
    schema_ui.render()
elif menu == "📄 문서 벡터화":
    from pages import vectorize_ui
    vectorize_ui.render()
elif menu == "🔍 통합 검색(QA/RAG)":
    from pages import search_ui
    search_ui.render()
elif menu == "💬 프롬프트 관리":
    from pages import prompt_template_ui
    prompt_template_ui.render()
elif menu == "🔗 데이터 병합/비교":
    from pages import file_merge_ui
    file_merge_ui.render()
elif menu == "📊 관계/통계 시각화":
    from pages import visualize_ui
    visualize_ui.render()
elif menu == "🕑 이력 관리":
    from pages import edit_ui
    edit_ui.render()
elif menu == "⚙️ 사용자 설정":
    from pages import settings_ui
    settings_ui.render()
