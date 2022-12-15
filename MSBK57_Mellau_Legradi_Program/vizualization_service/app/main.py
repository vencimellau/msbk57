import sys, os
sys.path.append('../..')
import app.auth_module as auth_module


from fastapi import FastAPI, WebSocket, Request, Response, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware


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
    return {"message": "Hello VIZ"}


#IF NOT LOGGED IN RETURN TO LOGIN
@app.exception_handler(auth_module.NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: auth_module.NotAuthenticatedException):
    return RedirectResponse(url='http://localhost:8001/login')
