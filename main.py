from fastapi import Body, FastAPI
from pydantic import BaseModel
from typing import Optional, List

class Blog(BaseModel):
    id: int
    title: str
    subtitle: str
    author: str
    date: str
    category: str

class BlogUpdate(BaseModel):
    title: str
    subtitle: str
    author: str
    date: str
    category: str

app = FastAPI()

app.title = "API Rest blog"
app.version = "0.1.1"

blog_list = [
    {
        "id": 1,
        "title": "Estadistica para Machine Learning",
        "subtitle": "Este es un blog para...",
        "author": "Nicolas Oses",
        "date": "3/2/2025",
        "category": "data science"
    },
    {
        "id": 2,
        "title": "Estadistica para Machine Learning",
        "subtitle": "Este es un blog para...",
        "author": "Nicolas Oses",
        "date": "3/2/2025",
        "category": "programacion"
    }
]

@app.get("/", tags=['Home'])
async def root():
    return {"message": "Bienvenido a la API Rest de mi blog de programación"}



@app.get("/blogs", tags=['Blog'])
async def all_blogs() -> List[Blog]:
    return blog_list



@app.get("/blogs/{id}", tags=['Blog'])
async def get_blog(id: int) -> Blog:
    for blog in blog_list:
        if blog['id'] == id:
            return blog
    return []



@app.get("/blogs/", tags=['Blog'])
async def get_blog_by_category(category: str) -> Blog:
    for blog in blog_list:
        if blog['category'] == category:
            return blog
    return []



@app.post("/blogs", tags=['Blog'])
async def create_blog(blog: Blog) -> List[Blog]:
    blog_list.append(blog.model_dump())
    return blog_list



@app.put("/blogs/{id}", tags=['Blog'])
async def update_blog(id: int, blog: BlogUpdate) -> List[Blog]:
    for item in blog_list:
        if item['id'] == id:
            item['title'] = blog.title
            item['subtitle'] = blog.subtitle
            item['author'] = blog.author
            item['date'] = blog.date
            item['category'] = blog.category
    return blog_list



@app.delete("/blogs/{id}", tags=['Blog'])
async def delete_blog(id: int) -> List[Blog]:
    for blog in blog_list:
        if blog['id'] == id:
            blog_list.remove(blog)
    return blog_list