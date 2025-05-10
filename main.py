from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import technology_router, project_router, token_router
from db.database import engine, Base

# crear todas las tablas del modelo en la base de datos 
Base.metadata.create_all(bind=engine)

# Instanciacion de FastApi e Informacion de nuestra APP
app = FastAPI()
app.title = "API Rest Portafolio Personal"
app.version = "0.1.2"

origins = [
    "https://nicolasoses.dev/",
    "http://localhost:5173",  # Para desarrollo local con React
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metodo Home 
@app.get("/", tags=['Home'])
async def root():
    return {"message": "Bienvenido a la API Rest de mi portafolio profesional"}

# rutas
app.include_router(technology_router.router, prefix="/api/technologies", tags=["Tecnologías"])
app.include_router(project_router.router, prefix="/api/projects", tags=["Proyectos"])
app.include_router(token_router.router, prefix="/api/token", tags=["Seguridad"])

