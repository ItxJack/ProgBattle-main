from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import FastAPI, HTTPException, status
from fastapi import Depends
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel


from jose import jwt #https://pypi.org/project/python-jose/ = pip install python-jose
 
from models import UserModel
 
JWT_SECRET="rahulranjanrawzz"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto") #pip install bcrypt
# save token to oauth2_scheme
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="user/signin")
COOKIE_NAME="Authorization"
 
# create Token
def create_access_token(user):
    try:
        payload={
            "username":user.username,
            "email":user.email,
            "role":user.role.value,
            "active":user.is_active,
 
        }
        return  jwt.encode(payload,key=JWT_SECRET,algorithm=ALGORITHM)
    except Exception as ex:
        print(str(ex))
        raise ex
 
# create verify Token
def verify_token(token):
    try:
        payload=jwt.decode(token,key=JWT_SECRET)
        return payload
    except Exception as ex:
        print(str(ex))
        raise ex
 
# password hash
def  get_password_hash(password):
    return pwd_context.hash(password)
 
# password verify
def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)
 
def get_current_user_from_token(token:str=Depends(oauth2_scheme)):
    user= verify_token(token)
    return user
 
def get_current_user_from_cookie(request:Request):
    token=request.cookies.get(COOKIE_NAME)
    if token:
        user = verify_token(token)
        return user