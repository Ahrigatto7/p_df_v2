import streamlit as st
import requests

API_BASE = "http://localhost:8000"  # Streamlit Cloud 배포 시 외부 URL로 교체 필요

st.header("🛠 CRUD / 이력 관리")

st.subheader("📋 프롬프트 목록")
try:
    response = requests.get(f"{API_BASE}/prompt_templates")
    templates = response.json()
except Exception as e:
    st.error(f"데이터 불러오기 실패: {e}")
    st.stop()

selected_name = st.selectbox("수정할 프롬프트 선택", [t["name"] for t in templates])
selected_template = next((t for t in templates if t["name"] == selected_name), None)

if selected_template:
    st.markdown("### ✏️ 프롬프트 수정")
    new_template = st.text_area("프롬프트 내용", value=selected_template["template"], height=200)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 수정 저장"):
            try:
                res = requests.put(f"{API_BASE}/prompt_templates/{selected_name}", json={"template": new_template})
                if res.status_code == 200:
                    st.success("✅ 수정이 완료되었습니다.")
                else:
                    st.error(f"❌ 수정 실패: {res.text}")
            except Exception as e:
                st.error(f"수정 요청 실패: {e}")

    with col2:
        if st.button("🗑 삭제"):
            try:
                res = requests.delete(f"{API_BASE}/prompt_templates/{selected_name}")
                if res.status_code == 200:
                    st.success("🗑 삭제 완료")
                else:
                    st.error(f"삭제 실패: {res.text}")
            except Exception as e:
                st.error(f"삭제 요청 실패: {e}")

