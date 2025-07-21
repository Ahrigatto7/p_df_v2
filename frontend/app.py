import streamlit as st
from pages import vectorize_ui, search_ui, document_ui, prompt_template_ui, history_log_ui

st.sidebar.title("AI 문서 QA 시스템")
page = st.sidebar.radio("메뉴 선택", (
    "문서 업로드", "검색/질의응답", "문서 관리", "프롬프트 관리", "히스토리 로그"
))

if page == "문서 업로드":
    vectorize_ui.show()
elif page == "검색/질의응답":
    search_ui.show()
elif page == "문서 관리":
    document_ui.show()
elif page == "프롬프트 관리":
    prompt_template_ui.show()
elif page == "히스토리 로그":
    history_log_ui.show()
