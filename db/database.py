import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")  
HOST = os.getenv("HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")

URL_DATABASE = f"postgresql://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# conexión con la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()