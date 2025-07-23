import streamlit as st
import requests

st.header("통합 RAG 검색(QA)")

question = st.text_input("질문 입력")
sources = st.multiselect(
    "검색 범위",
    ["PDF", "DOCX", "TXT", "HTML", "MD", "JSON", "XLSX", "규칙", "사례", "용어"],
    default=["PDF", "DOCX", "TXT", "HTML", "MD", "JSON", "XLSX", "규칙", "사례", "용어"],
)

if st.button("검색"):
    if not question.strip():
        st.warning("질문을 입력해주세요.")
        st.stop()

    try:
        res = requests.post(
            "http://localhost:8000/search",
            json={"question": question, "sources": sources}
        )

        if res.status_code == 200:
            data = res.json()
            for doc in data.get("sources", []):
                st.markdown(f"**[{doc['doc_type']}]** {doc['title']} : {doc['excerpt']}")
            st.success("AI 답변: " + data.get("answer", ""))
        else:
            st.error(f"❌ 오류 발생: {res.status_code} - {res.text}")

    except requests.exceptions.ConnectionError:
        st.error("❌ 백엔드 서버에 연결할 수 없습니다. FastAPI 서버가 실행 중인지 확인하세요.")

