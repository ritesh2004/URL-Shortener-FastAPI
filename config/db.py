from sqlmodel import create_engine, SQLModel, Session
from app.config.config import settings


engine = create_engine(str(settings.MYSQL_DATABASE_URI), echo=True)

SessionLocal = Session(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
        
