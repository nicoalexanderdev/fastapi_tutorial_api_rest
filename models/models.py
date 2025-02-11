from sqlalchemy import Integer, String, ForeignKey, Column, Table, DateTime, func
from sqlalchemy.orm import relationship
from db.database import Base

# Tabla intermedia para la relación muchos a muchos
project_technology = Table(
    'project_technology', Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id', ondelete="CASCADE"), primary_key=True),
    Column('technology_id', Integer, ForeignKey('technologies.id', ondelete="CASCADE"), primary_key=True)
)

class Technology(Base):
    __tablename__ = 'technologies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    projects = relationship("Project", secondary=project_technology, back_populates="technologies")

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), unique=True, nullable=False, index=True)
    urlname = Column(String(50), unique=True, nullable=False)
    subtitle = Column(String(100))
    description = Column(String(200))
    url = Column(String, unique=True)
    monthyear = Column(String(20))
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    technologies = relationship("Technology", secondary=project_technology, back_populates="projects")
