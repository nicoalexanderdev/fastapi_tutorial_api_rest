from fastapi import FastAPI
from routers import technology_router
from db.database import engine, Base

# crear todas las tablas del modelo en la base de datos 
Base.metadata.create_all(bind=engine)

# Instanciacion de FastApi e Informacion de nuestra APP
app = FastAPI()
app.title = "API Rest Portafolio Personal"
app.version = "0.1.2"

# Metodo Home 
@app.get("/", tags=['Home'])
async def root():
    return {"message": "Bienvenido a la API Rest de mi portafolio profesional"}

app.include_router(technology_router.router, prefix="/api/technologies", tags=["Tecnologías"])

