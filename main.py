from fastapi import FastAPI

app = FastAPI()

app.title = "API Rest blog"
app.version = "0.1.1"

blog = [
    {
        "id": 1,
        "title": "Estadistica para Machine Learning",
        "subtitle": "Este es un blog para...",
        "author": "Nicolas Oses",
        "fecha": "3/2/2025"
    }
]

@app.get("/", tags=['Home'])
async def root():
    return {"message": "Bienvenido a la API Rest de mi blog de programación"}

@app.get("/blogs", tags=['Blog'])
async def all_blogs():
    return blog