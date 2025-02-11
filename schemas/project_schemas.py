from pydantic import BaseModel, Field
from typing import List
from tech_schemas import TechnologiesBase
import datetime

class ProjectBase(BaseModel):
    id: int
    title: str
    urlname: str
    subtitle: str
    description: str
    url: str
    monthyear: str
    created_at: str
    updated_at: str
    technologies: List[TechnologiesBase]


class ProjectCreateBase(BaseModel):
    title: str = Field(min_length=5, max_length=20)
    urlname: str
    subtitle: str
    description: str
    url: str
    monthyear: str
    created_at: str = Field(default= str(datetime.date.today()))
    updated_at: str = Field(default= str(datetime.date.today()))
    technologies: List[TechnologiesBase]


class ProjectUpdateBase(BaseModel):
    title: str
    urlname: str
    subtitle: str
    description: str
    url: str
    monthyear: str
    updated_at: str = Field(default= str(datetime.date.today()))
    technologies: List[TechnologiesBase]