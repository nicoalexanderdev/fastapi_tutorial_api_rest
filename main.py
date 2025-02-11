from fastapi import Body, FastAPI, HTTPException, Depends
from typing import Optional, List, Annotated
from sqlalchemy.exc import IntegrityError

from schemas.tech_schemas import TechnologiesBase
from db.database import engine, SessionLocal, get_db
import models.models as _models
from models.models import Technology
from sqlalchemy.orm import Session


# Instanciacion de FastApi e Informacion de nuestra APP
app = FastAPI()
app.title = "API Rest Portafolio Personal"
app.version = "0.1.2"


# crear todas las tablas del modelo en la base de datos 
_models.Base.metadata.create_all(bind=engine)


# creacion de la injeccion de dependencia con la base de datos
db_dependency = Annotated[Session, Depends(get_db)]


# Metodo Home 
@app.get("/", tags=['Home'])
async def root():
    return {"message": "Bienvenido a la API Rest de mi portafolio profesional"}


# Metodos para la tabla technologies
@app.post("/api/technologies", tags=['Tecnologías'])
async def add_technology(technology: TechnologiesBase, db:db_dependency):
    try:
        tech = Technology(name=technology.name)
        db.add(tech)
        db.commit()
        db.refresh(tech)  # 🔹 Actualiza el objeto con el ID generado
        return {"message": "Éxito", "technology": tech}
    except IntegrityError:
        db.rollback()  # 🔹 Revierte la transacción en caso de error
        raise HTTPException(status_code=400, detail="La tecnología ya existe")
    

@app.get("/api/technologies", tags=['Tecnologías'])
async def get_all_technologies(db: db_dependency):
    technologies = db.query(Technology).all()
    return {"technologies": technologies}
