from .models import Document
from sqlalchemy.orm import Session

def create_document(session: Session, title, doc_type, content, meta):
    doc = Document(title=title, doc_type=doc_type, content=content, meta=meta)
    session.add(doc)
    session.commit()
    return doc

def update_document(session: Session, doc_id, **kwargs):
    doc = session.query(Document).get(doc_id)
    for k, v in kwargs.items():
        setattr(doc, k, v)
    session.commit()
    return doc

def delete_document(session: Session, doc_id):
    doc = session.query(Document).get(doc_id)
    session.delete(doc)
    session.commit()
    return True

def list_documents(session: Session, doc_type=None):
    q = session.query(Document)
    if doc_type:
        q = q.filter(Document.doc_type == doc_type)
    return q.all()
