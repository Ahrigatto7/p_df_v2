import streamlit as st
import requests

def render():
    st.header("규칙/사례/용어/문서 통합 벡터화")
    files = st.file_uploader("파일 업로드", accept_multiple_files=True)
    doc_type = st.selectbox("유형", ["규칙", "사례", "용어", "PDF"])
    if st.button("업로드/임베딩"):
        for file in files:
            res = requests.post(
                "http://localhost:8000/vectorize",
                files={"file": (file.name, file, file.type)},
                data={"doc_type": doc_type}
            )
            st.success(res.json())