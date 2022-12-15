import sys, os
sys.path.append('../..')
import app.auth_module as auth_module

from fastapi import FastAPI, WebSocket, Request, Response, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# import sqlalchemy
# from sqlalchemy import insert

ratings_extract = "table"
ratings_transform = "table"
ratings_fact = "table"

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


origins = [
    "http://localhost",
    "http://localhost:8001",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello ETL"}

@app.get("/ETL")
async def root(user =Depends(auth_module.manager)):
    return {"message": "Hello ETL"}

@app.get("/video", response_class=FileResponse)
async def video():
    return "app/static/data/video.mp4"

@app.get("/stream")
async def stream(request: Request):
    response = templates.TemplateResponse("streamingapp.html", {"request": request})
    return response

class Rating(BaseModel):
    movieID: str
    userID: str
    rating : str

@app.post("/rate",  response_model=Rating)
async def rate( rate : Rating):
    insert(ratings_extract).values(movieID=rate['movieID'], userID=rate['userID'], rating = rate['rating'])
    #Transform
    movieID = int(rate['movieID'])
    userID = int(rate['userID'])
    rating = float(rate['rating'])
    insert(ratings_transform).values(movieID=movieID, userID=userID, rating = rating)
    insert(ratings_fact).values(movieID=movieID, userID=userID, rating = rating)
    return rate 

@app.post("/watchmin")
async def watchmin(request: Request):
    get_inp_url = "input"
    return RedirectResponse(url=get_inp_url)    


#IF NOT LOGGED IN RETURN TO LOGIN
@app.exception_handler(auth_module.NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: auth_module.NotAuthenticatedException):
    return RedirectResponse(url='http://localhost:8001/login')

