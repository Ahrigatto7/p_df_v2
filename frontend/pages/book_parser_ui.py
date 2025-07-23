import streamlit as st
import pandas as pd
from io import BytesIO

from analyze_text_to_db import (
    extract_text_from_pdf,
    extract_sections,
    save_to_all_formats,
)


def main():
    st.title("문서 개념/사례 추출")
    uploaded = st.file_uploader("PDF 또는 텍스트 파일 업로드", type=["pdf", "txt"])
    text_input = st.text_area("또는 텍스트 입력")

    if st.button("추출 시작"):
        text = ""
        if uploaded:
            if uploaded.name.lower().endswith(".pdf"):
                text = extract_text_from_pdf(uploaded.read())
            else:
                text = uploaded.read().decode("utf-8", errors="ignore")
        text += "\n" + text_input
        if not text.strip():
            st.warning("분석할 텍스트를 입력하거나 파일을 업로드하세요.")
            return
        concepts, cases = extract_sections(text)
        paths = save_to_all_formats(concepts, cases, output="streamlit_output")

        records = [
            {"type": "concept", "text": t} for t in concepts
        ] + [{"type": "case", "text": t} for t in cases]
        df = pd.DataFrame(records)
        st.subheader("미리보기")
        st.dataframe(df)
        st.success("정리 완료! 아래에서 미리보기 또는 다운로드하세요.")

        with open(paths["excel"], "rb") as f:
            st.download_button("Excel 다운로드", f, file_name="extracted.xlsx")
        with open(paths["csv"], "rb") as f:
            st.download_button("CSV 다운로드", f, file_name="extracted.csv")
        with open(paths["sqlite"], "rb") as f:
            st.download_button("SQLite 다운로드", f, file_name="extracted.sqlite")


if __name__ == "__main__":
    main()
