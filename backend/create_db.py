from app.db.database import Base, engine
from app.models.task import Task

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")