import streamlit as st
import pandas as pd
import requests

API_BASE = "http://localhost:8000"

def render():
    st.header("📂 문서 관리 (유형별)")

    doc_type = st.selectbox("문서 유형 선택", ["규칙", "사례", "용어", "PDF"])
    try:
        res = requests.get(f"{API_BASE}/documents", params={"doc_type": doc_type})
        docs = res.json()
        df = pd.DataFrame(docs)
        st.dataframe(df[["id", "title", "doc_type", "created_at"]])
    except Exception as e:
        st.error(f"문서 불러오기 실패: {e}")
