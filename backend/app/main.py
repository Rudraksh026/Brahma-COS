from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.db.database import engine
from app.models.task import Base
from app.models.knowledge import Knowledge
from app.models.memory import Memory
from app.models.audit import Audit
from app.api.routes.tasks import router as task_router
from app.api.routes.chat import router as chat_router
from app.api.routes.upload import router as upload_router
from app.api.routes.memory import router as memory_router
from app.api.routes.audit import router as audit_router
from app.api.routes.agents import router as agents_router

Base.metadata.create_all(bind=engine)
app=FastAPI(title="BRAHMA COS Backend API",version="1.1.0")
origins=["http://localhost:3000","http://localhost:3001"]
if os.getenv("FRONTEND_ORIGIN"): origins.append(os.getenv("FRONTEND_ORIGIN"))
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(task_router); app.include_router(chat_router); app.include_router(upload_router); app.include_router(memory_router); app.include_router(audit_router); app.include_router(agents_router)
@app.get("/")
def root(): return {"message":"BRAHMA COS Backend is Running","database":"configured"}
@app.get("/health")
def health(): return {"status":"healthy"}
