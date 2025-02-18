from fastapi import HTTPException, Depends, APIRouter
from typing import List, Annotated
from sqlalchemy.exc import IntegrityError

from schemas.tech_schema import TechnologyBase, TechnologyCreate, TechnologyResponse
from db.database import get_db
from models.technology import TechnologyModel
from sqlalchemy.orm import Session

router = APIRouter()

# creacion de la injeccion de dependencia con la base de datos
db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=TechnologyResponse)
async def add_technology(technology: TechnologyCreate, db:db_dependency):
    try:
        tech = TechnologyModel(name=technology.name)
        db.add(tech)
        db.commit()
        db.refresh(tech)  
        return tech
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="La tecnología ya existe")
    

@router.get("/", response_model=List[TechnologyResponse])
async def get_all_technologies(db: db_dependency):
    try:
        technologies = db.query(TechnologyModel).all()
        return technologies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=TechnologyResponse)
async def get_technology_by_id(id: int, db: db_dependency):
    technology = db.query(TechnologyModel).filter(TechnologyModel.id == id).first()

    if not technology:
        raise HTTPException(status_code=404, detail="La tecnología no fue encontrada")
    
    return technology


@router.put("/{id}", response_model=TechnologyResponse)
async def update_technology(id: int, technology_data: TechnologyBase, db: db_dependency):
    technology = db.query(TechnologyModel).filter(TechnologyModel.id == id).first()

    if not technology:
        raise HTTPException(status_code=404, detail="La tecnología no fue encontrada")
    
    try:
        technology.name = technology_data.name

        db.commit()
        db.refresh(technology) 

        return technology
    except IntegrityError:
        db.rollback()  
        raise HTTPException(status_code=400, detail="Error de integridad. Posiblemente la tecnología ya existe.")
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
    

@router.delete("/{id}")
async def delete_technology(id: int, db: db_dependency):
    technology = db.query(TechnologyModel).filter(TechnologyModel.id == id).first()

    if not technology:
        raise HTTPException(status_code=404, detail="La tecnología no fue encontrada")
    
    try:
        db.delete(technology)
        db.commit()
        return {"message": str(f"Éxito al eliminar la tecnología con el ID: {id}")}
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="No se puede eliminar la tecnología porque está en uso.")
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")