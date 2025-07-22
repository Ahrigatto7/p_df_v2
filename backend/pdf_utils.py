from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import pandas as pd
import docx2txt
import json
import re
from collections import Counter
import os

def extract_pdf_text(file_path):
    reader = PdfReader(file_path)
    text = "".join(page.extract_text() or "" for page in reader.pages)
    return text.strip()

def extract_text(file_path, file_type="TXT"):
    """Return raw text from various document types"""
    file_type = file_type.upper()
    if file_type == "PDF":
        return extract_pdf_text(file_path)
    if file_type in {"TXT", "MD"}:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    if file_type == "HTML":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            return soup.get_text(separator=" ")
    if file_type == "JSON":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            data = json.load(f)
            return json.dumps(data)
    if file_type in {"XLSX", "EXCEL"}:
        df = pd.read_excel(file_path)
        return "\n".join("\t".join(map(str, row)) for row in df.values)
    if file_type == "DOCX":
        return docx2txt.process(file_path)
    return ""

def clean_text(text):
    """Remove unwanted patterns and duplicate whitespace"""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"페이지 \d+", "", text)
    text = text.replace("참조", "")
    return text.strip()

def split_text(text, max_length=400):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks, chunk = [], ""
    for s in sentences:
        if len(chunk) + len(s) <= max_length:
            chunk += " " + s
        else:
            if chunk.strip():
                chunks.append(chunk.strip())
            chunk = s
    if chunk.strip():
        chunks.append(chunk.strip())
    return [c for c in chunks if len(c) > 30]

def generate_tags(text, top_n=5):
    words = re.findall(r"[\w가-힣]{2,}", text.lower())
    freq = Counter(words)
    common = [w for w, _ in freq.most_common(top_n)]
    return common

def extract_and_split_pdf_text(file_path, max_length=400):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    text = text.strip()
    
    # 문장 단위로 분리 후 적절한 길이로 chunk 생성
    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += " " + sentence
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # 너무 짧은 건 제외
    return [chunk for chunk in chunks if len(chunk) > 30]
