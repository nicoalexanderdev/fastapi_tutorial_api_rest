from pydantic import BaseModel, Field
from typing import List, Optional
from tech_schema import TechnologyResponse
import datetime

class ProjectCreateBase(BaseModel):
    title: str = Field(min_length=5, max_length=20)
    urlname: str
    subtitle: str
    description: str
    github_url: str
    monthyear: str
    created_at: str = Field(default= str(datetime.date.today()))
    updated_at: str = Field(default= str(datetime.date.today()))
    technologies: Optional[List[int]] = []

class ProjectResponse(BaseModel):
    id: int
    title: str 
    urlname: str
    subtitle: str
    description: str
    github_url: str
    monthyear: str
    created_at: str 
    updated_at: str
    technologies: List[TechnologyResponse] = []  # Lista de tecnologías asociadas

    class Config:
        from_attributes = True

class ProjectUpdate(BaseModel):
    title: str
    urlname: str
    subtitle: str
    description: str
    github_url: str
    monthyear: str
    updated_at: str = Field(default= str(datetime.date.today()))
    technologies: Optional[List[int]] = []