import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.pdf_service import extract_text
from app.services.chunk_service import split_into_chunks
from app.services.embedding_service import generate_embedding
from app.repositories.knowledge_repository import semantic_search
from app.models.knowledge import Knowledge

router=APIRouter(prefix="/upload", tags=["Knowledge"])
UPLOAD_DIR="app/uploads"; os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_pdf(file: UploadFile=File(...), db: Session=Depends(get_db)):
    if not file.filename: raise HTTPException(400,"Filename required")
    if not file.filename.lower().endswith(".pdf"): raise HTTPException(400,"Only PDF files are supported")
    safe_name=os.path.basename(file.filename); path=os.path.join(UPLOAD_DIR,safe_name)
    with open(path,"wb") as f: f.write(await file.read())
    text=extract_text(path); chunks=split_into_chunks(text); stored=0; skipped=0
    for chunk in chunks:
        emb=generate_embedding(chunk)
        if not emb: skipped += 1; continue
        db.add(Knowledge(title=safe_name, content=chunk, embedding=emb)); stored += 1
    db.commit()
    return {"message":"Knowledge uploaded successfully","filename":safe_name,"chunks":len(chunks),"stored":stored,"skipped":skipped}

@router.get("/")
def list_uploads(db: Session=Depends(get_db)):
    rows=db.query(Knowledge.title).distinct().order_by(Knowledge.title).all()
    return [{"title":r[0]} for r in rows]

@router.get("/search")
def search_knowledge(q: str, db: Session=Depends(get_db)):
    return semantic_search(db,q)
