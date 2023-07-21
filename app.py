from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
posts = []

origins=[
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time", "x-total-count"],
)

# Post Mode
class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    # created_at: datetime = datetime.now()
    # published_at: Optional[datetime]
    # published: bool = False

# Lee la ruta principal
@app.get('/')
def read_root():
    return{"Welcome": "Trying FastApi"}

# Obtiene todos los datos.
@app.get('/posts')
def get_posts():
    return posts

# POST new data
@app.post('/posts')
def save_post(post: Post):
    post.id = str(uuid())
    # dict() lo convierte a un objeto clave valor JS
    posts.append(post.dict())
    print(post)
    # Devuelve el ultimo dato del array
    return posts[-1]

# Buscar por ID
@app.get('/posts/{post_id}')
def get_post(post_id:str):
    print(post_id)
    for post in posts:
        if post["id"] == post_id:
            return post
        raise HTTPException(status_code=404, detail="User Not Found")

# Eliminado
@app.delete('/posts/{post_id}')
def delete_post(post_id: str):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index)
            return {"message": "Post has been DELETED Successfully"}
    raise HTTPException(status_code=404, detail="User Not Found")

# Actualizado
@app.put('/posts/{post_id}')
def update_post(post_id:str, updatedPost: Post):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts[index]["title"] = updatedPost.title
            posts[index]["content"] = updatedPost.content
            posts[index]["author"] = updatedPost.author
            return {"message": "Post hasbenn updated successfully"}
    raise HTTPException(status_code=404, detail="User Not Found")