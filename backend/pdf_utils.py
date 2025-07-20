import fitz  # PyMuPDF
import pdfplumber
import pytesseract
from PIL import Image
import io

def extract_pdf_text_advanced(file_path):
    doc = fitz.open(file_path)
    all_texts = []

    # pdfplumber는 한 번만 open
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(doc):
            # 1. 텍스트 추출 (PyMuPDF)
            text = page.get_text("text")
            all_texts.append(f"== Page {i+1} ==\n{text}")

            # 2. 표 추출 (pdfplumber)
            tables = pdf.pages[i].extract_tables()
            for table in tables:
                table_str = "\n".join([", ".join(row) for row in table])
                all_texts.append(f"[Table on Page {i+1}]\n{table_str}")

            # 3. 이미지 추출+OCR
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                pil_img = Image.open(io.BytesIO(image_bytes))
                ocr_text = pytesseract.image_to_string(pil_img, lang='eng+kor')
                if ocr_text.strip():
                    all_texts.append(f"[Image OCR Page {i+1}-{img_index+1}]\n{ocr_text}")

    return "\n".join(all_texts)

def split_text_chunks(text, chunk_size=1000, overlap=100):
    tokens = text.split('\n')
    chunks = []
    i = 0
    while i < len(tokens):
        chunk = "\n".join(tokens[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks
