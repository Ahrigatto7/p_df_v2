import argparse
import os
import io
import sqlite3
import pandas as pd
from pdfminer.high_level import extract_text


def extract_text_from_pdf(data: bytes) -> str:
    """Extract text from PDF bytes"""
    with open("_tmp_pdf.pdf", "wb") as f:
        f.write(data)
    text = extract_text("_tmp_pdf.pdf")
    os.remove("_tmp_pdf.pdf")
    return text


def extract_sections(text: str):
    """Very naive concept/case extractor"""
    concepts, cases = [], []
    for para in [p.strip() for p in text.splitlines() if p.strip()]:
        low = para.lower()
        if "case" in low or "사례" in low or "example" in low:
            cases.append(para)
        else:
            concepts.append(para)
    return concepts, cases


def save_to_all_formats(concepts, cases, output="output"):
    os.makedirs(output, exist_ok=True)
    records = [{"type": "concept", "text": t} for t in concepts] + [
        {"type": "case", "text": t} for t in cases
    ]
    df = pd.DataFrame(records)
    csv_path = os.path.join(output, "extracted.csv")
    excel_path = os.path.join(output, "extracted.xlsx")
    sqlite_path = os.path.join(output, "extracted.sqlite")
    df.to_csv(csv_path, index=False)
    df.to_excel(excel_path, index=False)
    conn = sqlite3.connect(sqlite_path)
    df.to_sql("extracted", conn, if_exists="replace", index=False)
    conn.close()
    return {"csv": csv_path, "excel": excel_path, "sqlite": sqlite_path}


def main():
    parser = argparse.ArgumentParser(description="텍스트나 PDF에서 개념/사례 추출")
    parser.add_argument("input", help="텍스트 또는 PDF 파일 경로")
    parser.add_argument("--output", default="output", help="저장 폴더")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise FileNotFoundError(args.input)

    if args.input.lower().endswith(".pdf"):
        with open(args.input, "rb") as f:
            text = extract_text_from_pdf(f.read())
    else:
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()

    concepts, cases = extract_sections(text)
    save_to_all_formats(concepts, cases, args.output)
    print("Extraction complete. Files saved to", args.output)


if __name__ == "__main__":
    main()
