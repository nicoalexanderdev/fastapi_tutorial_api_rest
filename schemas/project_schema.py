from pydantic import BaseModel, Field
from typing import List, Optional
from .tech_schema import TechnologyResponse

class ProjectCreate(BaseModel):
    title: str = Field(min_length=5, max_length=20)
    urlname: str
    subtitle: str
    description: str
    github_url: str
    technologies: Optional[List[int]] = []

class ProjectResponse(BaseModel):
    id: int
    title: str 
    urlname: str
    subtitle: str
    description: str
    github_url: str
    technologies: List[TechnologyResponse] = []  # Lista de tecnologías asociadas

    class Config:
        from_attributes = True

class ProjectUpdate(BaseModel):
    title: str
    urlname: str
    subtitle: str
    description: str
    github_url: str
    technologies: Optional[List[int]] = []