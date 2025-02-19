from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from routers.token_router import decode_token
from schemas.project_schema import ProjectResponse, ProjectCreate, ProjectUpdate
from models.project import ProjectModel
from models.technology import TechnologyModel
from sqlalchemy.exc import IntegrityError

router = APIRouter()

# creacion de la injeccion de dependencia con la base de datos
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", response_model=ProjectResponse)
async def add_project(project_data: ProjectCreate, db: db_dependency, auth: Annotated[dict, Depends(decode_token)]):
    try:
        # Obtener tecnologías si están presentes
        technologies = []
        if project_data.technologies:
            technologies = db.query(TechnologyModel).filter(TechnologyModel.id.in_(project_data.technologies)).all()
            if not technologies:
                raise HTTPException(status_code=400, detail="Algunas tecnologías no existen")

        # Crear el proyecto
        project = ProjectModel(
            title=project_data.title,
            urlname=project_data.urlname,
            subtitle=project_data.subtitle,
            description=project_data.description,
            github_url=project_data.github_url,
            technologies=technologies  # Relación con tecnologías
        )
        db.add(project)
        db.commit()
        db.refresh(project)  
        return project
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El proyecto ya existe")
    

@router.get("/", response_model=List[ProjectResponse])
async def get_all_projects(db: db_dependency):
    try:
        projects = db.query(ProjectModel).all()
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/{id}", response_model=ProjectResponse)
async def get_project_by_id(id: int, db: db_dependency):
    project = db.query(ProjectModel).filter(ProjectModel.id == id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return project


@router.put("/{id}", response_model=ProjectResponse)
async def update_project(id: int, project_data: ProjectUpdate, db: db_dependency, auth: Annotated[dict, Depends(decode_token)]):
    project = db.query(ProjectModel).filter(ProjectModel.id == id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    technologies = []
    if project_data.technologies:
        technologies = db.query(TechnologyModel).filter(TechnologyModel.id.in_(project_data.technologies)).all()
        if not technologies:
            raise HTTPException(status_code=400, detail="Algunas tecnologías no existen")


    try:
        project.title = project_data.title
        project.subtitle = project_data.subtitle
        project.urlname = project_data.urlname
        project.description = project_data.description
        project.github_url = project_data.github_url
        project.technologies = technologies

        db.commit()
        db.refresh(project)

        return project

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad. Posiblemente el proyecto ya existe.")
    

@router.delete("/{id}")
async def delete_project(id: int, db: db_dependency, auth: Annotated[dict, Depends(decode_token)]):
    project = db.query(ProjectModel).filter(ProjectModel.id == id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    try:
        db.delete(project)
        db.commit()
        return {"message": str(f"Éxito al eliminar el proyecto con el Id {id}")}

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="No se puede eliminar el proyecto porque está en uso.")
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
