from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException,Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT


app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    rate:int = 5 #default to 5
    
my_posts = [{"title": "title of post 1", "content": "content of post 1","id": 1},
            {"title": "title of post 2", "content": "content of post 2","id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

@app.options("/posts")
def get_options(user_agent: Optional[str] = Header(None)):
    return {}


@app.post("/posts",status_code=HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    
    my_posts.append(post_dict)
    return {"data":post_dict}

@app.get("/posts/latestpost")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"post_detail":post}

@app.get("/posts/{id}")
def get_post(id: int,response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return{'message':f"post with id: {id} was not found"}
    return {"post_detail":post}



@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int,post: Post):

    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data':post_dict}

