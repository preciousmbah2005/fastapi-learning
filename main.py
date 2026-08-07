from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel 

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# Path operation or refered to a route
@app.get("/") # Decorator
def root(): # Function
    return {"message": "welcome to my api!"}

# request comes in with a  Get method and the url "/"

@app.get("/post")
def get_posts():
    return {"data": "This is your posts"}
    
@app.post("/createposts")
def create_posts(post: Post):
    print(post)
    print(post.model_dump())
    return {"data": post}

# title str, content str




