import os
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt

from db.database import get_db
from models.users import UserModel

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


def encode_token(payload: dict) -> str:
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def decode_token(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency) -> dict:
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user = db.query(UserModel).filter(UserModel.username == data['username']).first()
    return user

@router.post("/")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not user or form_data.password != user.password:
        raise HTTPException(status_code=401, detail='Incorrect username or password')
    
    token = encode_token({
        "username": user.username,
        "email": user.email
    })
    
    return { "access_token": token, "token_type": "bearer"}
