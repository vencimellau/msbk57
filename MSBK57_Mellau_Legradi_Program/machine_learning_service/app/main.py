import sys, os
sys.path.append('../..')
import app.auth_module as auth_module
import xgboost as xgb
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier


from fastapi import FastAPI, WebSocket, Request, Response, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

svd_model = "svd"

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
    return {"message": "Hello ML"}


#IF NOT LOGGED IN RETURN TO LOGIN
@app.exception_handler(auth_module.NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: auth_module.NotAuthenticatedException):
    return RedirectResponse(url='http://localhost:8001/login')

#LOGIN POST WHICH CREATES THE JWT TOKEN AND COKKIE WITH HELP OF MANAGER
@app.post("/predict_svd_score")
async def predict_svd_score(request: Request, response: Response):
    
    return {"score" : "8.7"}


#TEACH SVD FURTHER
@app.post("/teach_svd")
def teach_svd_score(request: Request, response: Response):
    d = request.json()
    train = [v for k,v in d.items() if k not in 'rating']
    output = d["rating"]
    response = keepLearning(svd_model,train,output)
    return response

def keepLearning(model_old, X_new, y_new):
  model_new = XGBClassifier().fit(X_new, y_new, xgb_model=model_old)
  return model_new