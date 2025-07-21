import streamlit as st
import requests

def render():
    st.header("📚 업로드된 문서 보기")
    res = requests.get("http://localhost:8000/documents")
    documents = res.json().get("documents", [])

    if not documents:
        st.info("현재 저장된 문서가 없습니다.")
        return

    for doc in documents:
        st.markdown(f"**{doc['filename']}** (type: {doc['doc_type']}) - page {doc['page_number']}")
        st.code(doc['content'], language="markdown")
