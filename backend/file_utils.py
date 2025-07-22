import io
import json
import pandas as pd
import pdfplumber
import docx
from bs4 import BeautifulSoup


def extract_text_from_pdf(path: str) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def extract_text_from_docx(path: str) -> str:
    document = docx.Document(path)
    return "\n".join(p.text for p in document.paragraphs)


def extract_text_from_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_text_from_html(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")
    return soup.get_text(separator=" ")


def extract_text_from_md(path: str) -> str:
    return extract_text_from_txt(path)


def extract_text_from_json(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        data = json.load(f)
    return json.dumps(data, ensure_ascii=False)


def extract_text_from_excel(path: str) -> str:
    df = pd.read_excel(path, engine="openpyxl")
    return df.to_csv(index=False)


EXTRACTORS = {
    "PDF": extract_text_from_pdf,
    "DOCX": extract_text_from_docx,
    "TXT": extract_text_from_txt,
    "HTML": extract_text_from_html,
    "MD": extract_text_from_md,
    "JSON": extract_text_from_json,
    "XLSX": extract_text_from_excel,
}


def extract_text(path: str, doc_type: str) -> str:
    doc_type = doc_type.upper()
    extractor = EXTRACTORS.get(doc_type)
    if not extractor:
        raise ValueError(f"Unsupported document type: {doc_type}")
    return extractor(path)
