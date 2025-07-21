from PyPDF2 import PdfReader
import re

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
