from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel 
from random import randrange 

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# Storing posts in a list of dictionaries
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

# Path operation or refered to a route
@app.get("/") # Decorator
def root(): # Function
    return {"message": "welcome to my api!"}

# request comes in with a  Get method and the url "/"

@app.get("/posts")
def get_posts():
    return {"data": my_posts}
    
@app.post("/posts")
def create_posts(post: Post):
    # print(post)
    # print(post.model_dump())
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}
# title str, content str

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    print(post)
    return {"post_detail": post}



