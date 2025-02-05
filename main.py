from fastapi import Body, FastAPI

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
async def all_blogs():
    return blog_list

@app.get("/blogs/{id}", tags=['Blog'])
async def get_blog(id: int):
    for blog in blog_list:
        if blog['id'] == id:
            return blog
    return []

@app.get("/blogs/", tags=['Blog'])
async def get_blog_by_category(category: str):
    for blog in blog_list:
        if blog['category'] == category:
            return blog
    return []

@app.post("/blogs", tags=['Blog'])
async def create_blog(id: int = Body(), title: str = Body(), subtitle: str = Body(), author: str = Body(), date: str = Body(), category: str = Body()):
    blog_list.append(
        {
            "id" : id,
            "title" : title,
            "subtitle" : subtitle,
            "author" : author,
            "date" : date,
            "category" : category
        }
    )
    return blog_list

@app.put("/blogs/{id}", tags=['Blog'])
async def update_blog(id: int, title: str = Body(), subtitle: str = Body(), author: str = Body(), date: str = Body(), category: str = Body()):
    for blog in blog_list:
        if blog['id'] == id:
            blog['title'] = title
            blog['subtitle'] = subtitle
            blog['author'] = author
            blog['date'] = date
            blog['category'] = category
    return blog_list

@app.delete("/blogs/{id}", tags=['Blog'])
async def delete_blog(id: int):
    for blog in blog_list:
        if blog['id'] == id:
            blog_list.remove(blog)
    return blog_list