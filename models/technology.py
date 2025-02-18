from sqlalchemy import Integer, String, ForeignKey, Column, Table, DateTime, func
from sqlalchemy.orm import relationship
from db.database import Base
from .project import project_technology

class TechnologyModel(Base):
    __tablename__ = 'technologies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    projects = relationship("ProjectModel", secondary=project_technology, back_populates="technologies")