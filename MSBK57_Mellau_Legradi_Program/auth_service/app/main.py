from fastapi import Depends, FastAPI, HTTPException, status, Request, Response
from fastapi.responses import RedirectResponse


from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi.middleware.cors import CORSMiddleware


import app.auth_module as auth_module





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

#IF NOT LOGGED IN RETURN TO LOGIN
@app.exception_handler(auth_module.NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: auth_module.NotAuthenticatedException):
    return RedirectResponse(url='/login')    

#RETURNS LOGIN PAGE OR MAIN PAGE IF ALREADY LOGGED IN
@app.get("/login")
async def login(request: Request):
    token = await auth_module.manager._get_token(request)
    if token:
        response = templates.TemplateResponse("logged_in.html", {"request": request})
    else:
        response = templates.TemplateResponse("login.html", {"request": request})
    return response

#LOGIN POST WHICH CREATES THE JWT TOKEN AND COKKIE WITH HELP OF MANAGER
@app.post("/login")
async def login(request: Request, response: Response):
    d = await request.json()
    user = auth_module.authenticate_user(auth_module.db, d["username"], d["password"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username = d["username"]
    access_token = auth_module.manager.create_access_token(
        data={'sub': username}
    )
    auth_module.manager.set_cookie(response, access_token)
    return access_token

#LOGOUT WHICH TERMINATES THE JWT TOKEN AND COOKIE
@app.get("/logout")
async def logout(request: Request, response: Response):
    print(response)
    response = templates.TemplateResponse("login.html", {"request": request, "title": "Login", "current_user": ""})
    response.delete_cookie(key="access-token")
    return response

@app.get("/")
async def root():
    return {"message": "Welcome"}

#RETURNS USER INFORMATION DB
@app.get('/protected')
def protected_route(user =Depends(auth_module.manager)):
    return user

#RETURNS TOKEN AND USER INFORMATION
@app.get('/user')
async def protected_route(request : Request, user =Depends(auth_module.manager)):
    token = await auth_module.manager._get_token(request)
    user = await auth_module.manager.get_current_user(token)
    return user

#LOGGED IN PAGE
@app.get("/logged_in")
async def logged_in(request: Request, user =Depends(auth_module.manager)):
    response = templates.TemplateResponse("logged_in.html", {"request": request})
    return response
