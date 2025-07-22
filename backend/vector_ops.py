from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from .pdf_utils import extract_text, clean_text, split_text, generate_tags
from .db import get_db
from .models import create_document
import os
import tempfile

def vectorize_document(chunks, meta):
    """
    텍스트 청크와 메타데이터를 받아 벡터 DB에 저장합니다.
    """
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory="./vector_db/chroma_db", embedding_function=embeddings)
    docs = [{"page_content": chunk, "metadata": meta} for chunk in chunks]
    vectordb.add_documents(docs)
    return {"msg": "임베딩 완료", "count": len(chunks)}

def vectorize_file(file, doc_type="PDF", meta=None):
    """
    파일 객체를 받아 텍스트 추출, 벡터화, DB 저장을 모두 처리합니다.
    """
    if meta is None:
        meta = {}

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.read())
        path = tmp.name

    try:
        text = extract_text(path, doc_type)
        text = clean_text(text)
        chunks = split_text(text)
        tags = generate_tags(text)
        meta["doc_type"] = doc_type
        meta["filename"] = os.path.basename(path)

        # 벡터DB 저장
        vectorize_document(chunks, meta)

        # SQL DB 저장
        with next(get_db()) as db:
            for idx, chunk in enumerate(chunks):
                create_document(db, meta["filename"], doc_type, idx, chunk)

        return {"msg": "업로드 및 저장 완료", "총청크수": len(chunks), "tags": tags}

    finally:
        os.remove(path)

def hybrid_search(query, sources=None):
    """
    쿼리와 소스 필터를 받아 벡터DB에서 유사도 검색을 수행합니다.
    """
    vectordb = Chroma(persist_directory="./vector_db/chroma_db")
    filters = {"doc_type": {"$in": sources}} if sources else None
    results = vectordb.similarity_search(query, k=5, filter=filters)

    sources_out = []
    for r in results:
        snippet = r.page_content[:100]
        if query in r.page_content:
            snippet = r.page_content.replace(query, f"**{query}**")[:200]
        sources_out.append({
            "title": r.metadata.get("filename", ""),
            "doc_type": r.metadata.get("doc_type", ""),
            "excerpt": snippet
        })

    answer = " ".join([r.page_content for r in results])[:300]
    return {"answer": answer, "sources": sources_out}
