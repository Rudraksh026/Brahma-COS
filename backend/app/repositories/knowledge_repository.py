import math
from sqlalchemy.orm import Session
from app.db.database import is_sqlite
from app.models.knowledge import Knowledge
from app.services.embedding_service import generate_embedding

def _cosine(a, b):
    if not a or not b or len(a) != len(b): return -1.0
    dot = sum(x*y for x,y in zip(a,b)); na=math.sqrt(sum(x*x for x in a)); nb=math.sqrt(sum(y*y for y in b))
    return dot/(na*nb) if na and nb else -1.0

def semantic_search(db: Session, query: str, top_k: int = 5):
    embedding = generate_embedding(query)
    if not embedding:
        return []
    if is_sqlite:
        rows = db.query(Knowledge).all()
        ranked = sorted((( _cosine(embedding, r.embedding), r) for r in rows if r.embedding), key=lambda x:x[0], reverse=True)[:top_k]
        return [{"id": r.id, "title": r.title, "content": r.content, "score": round(score, 4)} for score,r in ranked]
    from sqlalchemy import text
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    result = db.execute(text("SELECT id,title,content,1-(embedding <=> CAST(:embedding AS vector)) AS score FROM knowledge WHERE embedding IS NOT NULL ORDER BY embedding <=> CAST(:embedding AS vector) LIMIT :top_k"), {"embedding": embedding_str, "top_k": top_k})
    return [{"id": r.id, "title": r.title, "content": r.content, "score": float(r.score) if r.score is not None else None} for r in result.fetchall()]
