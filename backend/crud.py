from .models import Document
from sqlalchemy.orm import Session


def create_document(
    session: Session, filename: str, doc_type: str, page_number: int, content: str, tags=None
) -> Document:
    """Create a document record."""
    doc = Document(
        filename=filename,
        doc_type=doc_type,
        page_number=page_number,
        content=content,
        tags=tags or [],
    )
    session.add(doc)
    session.commit()
    session.refresh(doc)
    return doc

def update_document(session: Session, doc_id: int, **kwargs) -> Document:
    """Update a document record."""
    doc = session.query(Document).get(doc_id)
    if not doc:
        return None
    for k, v in kwargs.items():
        if hasattr(doc, k):
            setattr(doc, k, v)
    session.commit()
    session.refresh(doc)
    return doc

def delete_document(session: Session, doc_id: int) -> bool:
    doc = session.query(Document).get(doc_id)
    if not doc:
        return False
    session.delete(doc)
    session.commit()
    return True

def list_documents(session: Session, doc_type: str = None):
    q = session.query(Document)
    if doc_type:
        q = q.filter(Document.doc_type == doc_type)
    return q.order_by(Document.created_at.desc()).all()


def save_extracted_chunks(session: Session, filename: str, doc_type: str, chunks, tags=None):
    """Save multiple chunks of a document."""
    for idx, chunk in enumerate(chunks):
        create_document(session, filename, doc_type, idx + 1, chunk, tags=tags)
