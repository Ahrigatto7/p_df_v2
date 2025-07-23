import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.header("❓ Q&A 관리")

try:
    qas = requests.get(f"{API_BASE}/qa").json().get("qas", [])
except Exception as e:
    st.error(f"데이터 불러오기 실패: {e}")
    st.stop()

st.subheader("목차")
for qa in qas:
    st.markdown(f"- {qa['question']}")

if qas:
    ids = [str(q['id']) for q in qas]
    selected_id = st.selectbox("편집할 항목", ids)
    current = next(q for q in qas if str(q['id']) == selected_id)

    question = st.text_input("질문", value=current['question'])
    answer = st.text_area("답변", value=current['answer'], height=200)
    if st.button("수정 저장"):
        res = requests.put(f"{API_BASE}/qa/{selected_id}", json={
            "question": question,
            "answer": answer
        })
        if res.status_code == 200:
            st.success("✅ 수정 완료")
        else:
            st.error(res.text)
else:
    st.info("저장된 Q&A가 없습니다.")

st.markdown("---")

st.subheader("새 Q&A 추가")
new_q = st.text_input("새 질문", key="new_q")
new_a = st.text_area("새 답변", key="new_a", height=200)
if st.button("추가"):
    res = requests.post(f"{API_BASE}/qa", json={"question": new_q, "answer": new_a})
    if res.status_code == 200:
        st.success("✅ 추가 완료")
    else:
        st.error(res.text)
