from fastapi import FastAPI, Body

app = FastAPI()


# Path operation or refered to a route
@app.get("/") # Decorator
def root(): # Function
    return {"message": "welcome to my api!"}

# request comes in with a  Get method and the url "/"

@app.get("/post")
def get_posts():
    return {"data": "This is your posts"}
    
@app.post("/createposts")
def create_posts(payLoad: dict = Body(...)):
    print(payLoad)
    return {"message": "successfully created post"}


