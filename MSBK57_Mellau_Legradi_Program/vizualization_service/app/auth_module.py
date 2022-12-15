from datetime import timedelta

from fastapi_login import LoginManager

from passlib.context import CryptContext
from pydantic import BaseModel


#SECRET KEY FOR DECRYPTING THE ALREADY HASED PASSWORD
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#MOAKED DB
db = {
    "admin": {
        "username": "admin",
        "full_name": "admin",
        "email": "admin@admin.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class NotAuthenticatedException(Exception):
    pass

manager = LoginManager(
    SECRET_KEY, 'http://localhost:8001/login',
    use_cookie=True,
    default_expiry=timedelta(hours=12),
    custom_exception=NotAuthenticatedException
)

#GET CURRENT USER
@manager.user_loader()
async def return_current_user(user_id : str):
    user = get_user(db, user_id)
    return user


#CHECK PASS IN MOAKED DB
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#HASHES THE PASS
def get_password_hash(password):
    return pwd_context.hash(password)

#CHECKS USER IN MOAKED DB
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

#VERIFIES USER WITH THE HELP OF THE MOAKED DB
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user