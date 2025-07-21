import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

def vectorize_document(chunks, meta):
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory="./vector_db/chroma_db", embedding_function=embeddings)
    docs = [Document(page_content=chunk, metadata=meta) for chunk in chunks]
    vectordb.add_documents(docs)
    return {"msg": "임베딩 완료", "count": len(chunks)}

def vectorize_file(file, doc_type="PDF", meta=None):
    import tempfile
    from .pdf_utils import extract_pdf_text, split_text
    from .db import get_db
    from .crud import save_extracted_chunks

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.read())
        path = tmp.name

    if doc_type == "PDF":
        text = extract_pdf_text(path)
    else:
        text = file.read().decode()
    chunks = split_text(text)

    # DB 저장 로직 추가
    with next(get_db()) as db:
        save_extracted_chunks(db, os.path.basename(path), doc_type, chunks)

    meta = meta or {}
    meta['doc_type'] = doc_type
    return vectorize_document(chunks, meta)

def hybrid_search(query, sources=None):
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory="./vector_db/chroma_db", embedding_function=embeddings)
    filters = {"doc_type": {"$in": sources}} if sources else None
    retriever = vectordb.as_retriever(search_kwargs={"k": 5, "filter": filters})
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), retriever=retriever, return_source_documents=True)

    result = qa.run(query)
    relevant_docs = retriever.get_relevant_documents(query)

    sources_out = [{
        "title": r.metadata.get("filename", ""),
        "doc_type": r.metadata.get("doc_type", ""),
        "excerpt": r.page_content[:100]
    } for r in relevant_docs]

    return {"answer": result, "sources": sources_out}
