from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List
import datetime

'''
    {
        "id": 1,
        "title": "API Portafolio",
        "urlname": "api-portafolio",
        "subtitle": "Backend Robusto en Go para la Gestión de los proyectos de mi Portafolio Profesional",
        "description": "API RESTful desarrollada con Go y Gin-Gonic que proporciona un backend escalable y de alto rendimiento para la gestión de mis proyectos profesionales. Implementa una arquitectura limpia con patrones Repository y Service, integración con MongoDB Atlas para el almacenamiento persistente, y mejores prácticas de desarrollo como inyección de dependencias y manejo de configuración mediante variables de entorno. La API ofrece endpoints completos para operaciones CRUD, permitiendo una gestión eficiente de proyectos con características como validación de datos, manejo de errores personalizado y respuestas JSON estructuradas.",
        "technologies": [
            "GO",
            "MongoDB"
        ],
        "url": "https://github.com/nicoalexanderdev/api-portafolio",
        "monthyear": "Octubre 2024",
        "created_at": "2024-11-01T22:07:14.542Z",
        "updated_at": "2025-01-14T02:53:08.629Z"
    }
'''

app = FastAPI()

app.title = "API Rest Portafolio Personal"
app.version = "0.1.2"

class Project(BaseModel):
    id: int
    title: str
    urlname: str
    subtitle: str
    description: str
    technologies: List[str]
    url: str
    monthyear: str
    created_at: str
    updated_at: str


class ProjectCreate(BaseModel):
    id: int
    title: str = Field(min_length=5, max_length=20)
    urlname: str
    subtitle: str
    description: str
    technologies: List[str]
    url: str
    monthyear: str
    created_at: str = Field(default= str(datetime.date.today()))
    updated_at: str = Field(default= str(datetime.date.today()))


class ProjectUpdate(BaseModel):
    title: str
    urlname: str
    subtitle: str
    description: str
    technologies: List[str]
    url: str
    monthyear: str
    updated_at: str = Field(default= str(datetime.date.today()))


project_list: List[Project] = []



@app.get("/", tags=['Home'])
async def root():
    return {"message": "Bienvenido a la API Rest de mi portafolio profesional"}



@app.get("/projects", tags=['Project'])
async def all_projects() -> List[Project]:
    return project_list


@app.get("/projects/{id}", tags=['Project'])
async def get_project_by_id(id: int) -> Project:
    for project in project_list:
        if project.id == id:
            return project
    return []



@app.get("/projects/", tags=['Project'])
async def get_project_by_category(category: str) -> Project:
    for project in project_list:
        if project['category'] == category:
            return project
    return []



@app.post("/projects", tags=['Project'])
async def create_project(project: ProjectCreate) -> List[Project]:
    if project: 
        project_id = len(project_list) + 1
        new_project = Project(
            id=project_id,
            title=project.title,
            urlname=project.urlname,
            subtitle=project.subtitle,
            description=project.description,
            technologies=project.technologies,
            url=project.url,
            monthyear=project.monthyear,
            created_at=str(datetime.date.today()),
            updated_at=str(datetime.date.today())
        )
        project_list.append(new_project)
        return project_list
    else:
        print("error")



@app.put("/projects/{id}", tags=['Project'])
async def update_project(id: int, project: ProjectUpdate) -> List[Project]:
    for item in project_list:
        if item.id == id:
            item.title = project.title
            item.urlname = project.urlname
            item.subtitle = project.subtitle
            item.description = project.description
            item.technologies = project.technologies
            item.url = project.url
            item.monthyear = project.monthyear
            item.updated_at = str(datetime.date.today())
            
    return project_list



@app.delete("/projects/{id}", tags=['Project'])
async def delete_project(id: int) -> List[Project]:
    for project in project_list:
        if project.id == id:
            project_list.remove(project)
    return project_list