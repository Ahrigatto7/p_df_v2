# frontend/custom_pages/prompt_template_ui.py
import streamlit as st
import requests
import json

def render():
    st.header("📄 PromptTemplate 관리 및 테스트")

    # 템플릿 파일 목록 가져오기
    files = requests.get("http://localhost:8000/prompt_templates").json()["files"]
    selected = st.selectbox("🗂 프롬프트 선택", files)

    if selected:
        # 템플릿 내용 불러오기
        content = requests.get("http://localhost:8000/prompt_template", params={"filename": selected}).json()["content"]
        new_content = st.text_area("📝 내용 편집", content, height=300)

        if st.button("💾 저장"):
            res = requests.put(
                "http://localhost:8000/prompt_template",
                params={"filename": selected},
                data=new_content.encode()
            )
            st.success("✅ 저장 완료")

        st.markdown("---")
        st.subheader("⚙️ 프롬프트 테스트")

        # 사용자 변수 입력
        var_input = st.text_area("JSON 형식 변수 입력 (예: {\"context\": \"...\", \"question\": \"...\"})", height=150)

        if st.button("🚀 테스트 실행"):
            try:
                variables = json.loads(var_input)
                res = requests.post("http://localhost:8000/prompt_test", json={
                    "template": new_content,
                    "variables": variables
                })
                st.success("✅ 결과")
                st.write(res.json()["output"])
            except Exception as e:
                st.error(f"⚠️ 실행 실패: {e}")
