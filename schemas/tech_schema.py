from pydantic import BaseModel

class TechnologyBase(BaseModel):
    name: str

class TechnologyCreate(BaseModel):
    name: str

class TechnologyResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
