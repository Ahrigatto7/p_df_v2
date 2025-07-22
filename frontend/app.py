import streamlit as st
from custom_pages import (
    dashboard_ui,
    vectorize_ui,
    search_ui,
    document_ui,
    prompt_template_ui,
    history_log_ui,
    edit_ui,
    schema_ui,
    visualize_ui,
)


st.set_page_config(page_title="AI 문서 QA 시스템", layout="wide")
st.sidebar.title("AI 문서 QA 시스템")

# 각 페이지 모듈을 사전 형태로 관리하면 새로운 페이지를
# 추가하거나 순서를 변경하기가 쉬워집니다.
PAGES = {
    "대시보드": dashboard_ui,
    "문서 업로드": vectorize_ui,
    "검색/질의응답": search_ui,
    "문서 관리": document_ui,
    "프롬프트 관리": prompt_template_ui,
    "히스토리 로그": history_log_ui,
    "프롬프트 편집": edit_ui,
    "데이터 스키마": schema_ui,
    "시각화": visualize_ui,
}

selection = st.sidebar.radio("메뉴 선택", list(PAGES.keys()))

# 선택한 페이지의 render 함수를 호출하여 화면을 구성합니다.
page_module = PAGES.get(selection)
if page_module:
    page_module.render()
