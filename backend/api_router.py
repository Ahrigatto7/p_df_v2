from fastapi import APIRouter, UploadFile, File, Form, Body, HTTPException
from .vector_ops import vectorize_file, hybrid_search
from .db import engine
from .schema_utils import infer_schema_from_file, auto_create_schema_from_df

router = APIRouter()

@router.post("/infer_schema")
async def infer_schema(file: UploadFile = File(...)):
    try:
        schema, _ = infer_schema_from_file(file)
        return {"schema": schema}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create_schema")
async def create_schema(
    file: UploadFile = File(...), 
    table_name: str = Form(...)):
    try:
        _, df = infer_schema_from_file(file)
        msg = auto_create_schema_from_df(df, table_name, engine)
        return {"msg": msg}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/vectorize")
async def vectorize(
    file: UploadFile = File(...),
    doc_type: str = Form("PDF"),
):
    try:
        meta = {"filename": file.filename}
        return vectorize_file(file.file, doc_type, meta)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search")
def search(payload: dict = Body(...)):
    question = payload.get("question")
    sources = payload.get("sources", ["규칙", "사례", "용어", "PDF"])
    if not question:
        raise HTTPException(status_code=400, detail="질문이 필요합니다.")
    try:
        return hybrid_search(question, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/prompt_templates")
def get_prompt_list():
    from .prompt_templates import list_prompts
    return {"files": list_prompts()}

@router.get("/prompt_template")
def get_prompt(filename: str):
    from .prompt_templates import load_prompt
    return {"content": load_prompt(filename)}

@router.put("/prompt_template")
def update_prompt(filename: str, content: str = Body(...)):
    from .prompt_templates import save_prompt
    save_prompt(filename, content)
    return {"msg": "저장 완료"}
