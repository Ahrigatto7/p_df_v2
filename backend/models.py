from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime
from typing import Optional, List
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    doc_type = Column(String, index=True)
    page_number = Column(Integer)
    content = Column(Text)
    tags = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

# CRUD FUNCTIONS

def create_document(
    db: Session,
    filename: str,
    doc_type: str,
    page_number: int,
    content: str,
    tags: Optional[list] = None
) -> Document:
    """문서 생성"""
    doc = Document(
        filename=filename,
        doc_type=doc_type,
        page_number=page_number,
        content=content,
        tags=tags or []
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

def get_documents(
    db: Session,
    filename: Optional[str] = None,
    doc_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Document]:
    """조건별 문서 목록 조회"""
    query = db.query(Document)
    if filename:
        query = query.filter(Document.filename == filename)
    if doc_type:
        query = query.filter(Document.doc_type == doc_type)
    return query.offset(skip).limit(limit).all()

def get_document_by_id(db: Session, document_id: int) -> Optional[Document]:
    """ID로 단일 문서 조회"""
    return db.query(Document).filter(Document.id == document_id).first()

def update_document(
    db: Session,
    document_id: int,
    filename: Optional[str] = None,
    doc_type: Optional[str] = None,
    page_number: Optional[int] = None,
    content: Optional[str] = None
) -> Optional[Document]:
    """문서 수정"""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        return None
    if filename is not None:
        doc.filename = filename
    if doc_type is not None:
        doc.doc_type = doc_type
    if page_number is not None:
        doc.page_number = page_number
    if content is not None:
        doc.content = content
    try:
        db.commit()
        db.refresh(doc)
        return doc
    except SQLAlchemyError:
        db.rollback()
        return None

def delete_document(db: Session, document_id: int) -> bool:
    """문서 삭제"""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        return False
    try:
        db.delete(doc)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        return False
