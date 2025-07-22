from fastapi import APIRouter, UploadFile, File, Form, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from .db import get_db
from .vector_ops import vectorize_file, hybrid_search
from . import models

router = APIRouter()

@router.post("/vectorize")
async def vectorize(
    file: UploadFile = File(...),
    doc_type: str = Form("PDF"),
):
    meta = {"filename": file.filename}
    return vectorize_file(file.file, doc_type, meta)

@router.post("/search")
async def search(payload: Dict[str, Any] = Body(...)):
    question = payload.get("question")
    sources = payload.get("sources", ["규칙", "사례", "용어", "PDF"])
    return hybrid_search(question, sources=sources)

@router.get("/prompt_templates")
async def get_prompt_list():
    from .prompt_templates import list_prompts
    return {"files": list_prompts()}

@router.get("/prompt_template")
async def get_prompt(filename: str):
    from .prompt_templates import load_prompt
    return {"content": load_prompt(filename)}

@router.put("/prompt_template")
async def update_prompt(filename: str, content: str = Body(...)):
    from .prompt_templates import save_prompt
    save_prompt(filename, content)
    return {"msg": "저장 완료"}

@router.get("/documents")
async def list_documents(db: Session = Depends(get_db)):
    documents = db.query(models.Document).order_by(models.Document.created_at.desc()).limit(100).all()
    return {
        "documents": [
            {
                "id": doc.id,
                "filename": doc.filename,
                "doc_type": doc.doc_type,
                "page_number": doc.page_number,
                "content": doc.content,
                "created_at": doc.created_at.isoformat()
            }
            for doc in documents
        ]
    }
