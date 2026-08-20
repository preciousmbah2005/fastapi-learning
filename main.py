# Optional allows the rating field to be omitted or set to None.
from typing import Optional
from fastapi import FastAPI, Response, status
from fastapi.params import Body
from pydantic import BaseModel 
from random import randrange 

# Create the FastAPI application instance.
app = FastAPI()

# Pydantic model used to validate the body of POST requests.
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# Temporary in-memory storage; data is lost when the application restarts.
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]

# Return the post matching the supplied ID, or None if it does not exist.
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

# Return the list index of a post matching the supplied ID.
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

# Health-check or welcome endpoint for the API.
@app.get("/") # Decorator
def root(): # Function
    return {"message": "welcome to my api!"}

# Return all posts currently stored in memory.
@app.get("/posts")
def get_posts():
    return {"data": my_posts}
    
@app.post("/posts")
def create_posts(post: Post):
    # print(post)
    # print(post.model_dump())
    # Convert the validated Pydantic model into a dictionary and assign an ID.
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}
# title str, content str


# /posts/latest must be defined before /posts/{id} because FastAPI matches routes in order.
# If /posts/{id} were first, a request to /posts/latest would match it with id="latest",
# causing an error. By placing /posts/latest first, it gets priority and matches correctly.

@app.get("/posts/latest")
def get_latest_post():
    # The last item is treated as the newest post.
    post = my_posts[len(my_posts) -1]
    return {"latest_post": post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    # This route uses a path parameter named 'id'.
    # FastAPI will capture the segment after /posts/ and convert it to int.
    # For example, /posts/1 and /posts/2 are valid requests.
    # It may appear to only work for 1 because the current sample data
    # contains a post with id=1, and there is no post for other ids unless added.
    post = find_post(id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Post not found"}
    print(post)
    return {"post_detail": post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    # deleting post
    # find the index in the array that has required ID
    # my_post.pop(index)
    index = find_index_post(id)

    # Remove the post at the matching index.
    my_posts.pop(index)
    return {"message": "post was successfully deleted"}


