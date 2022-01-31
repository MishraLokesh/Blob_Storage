from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.user import Login
from sqlalchemy.sql import text
from config.db import conn
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from . import JWT_token


router = APIRouter(tags=['Authentication'])

def verify_password(plain_password, hashed_password):
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  return pwd_context.verify(plain_password, hashed_password)



@router.post('/login')
def login(login:OAuth2PasswordRequestForm = Depends()):
  s1 = text("SELECT * FROM blob.users where email = :username")
  user = conn.execute(s1, username=login.username).fetchall()
  if not user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Invalid Credentials",)
  
  q = text("SELECT password FROM blob.users where email = :username")
  hashed_pass = conn.execute(q, username=login.username).fetchall()[0][0]
  if not verify_password(login.password, hashed_pass):
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Incorrect Password",)

  # generate a JWT token and return it
  access_token = JWT_token.create_access_token(data={"sub": login.username})
  return {"access_token": access_token, "token_type": "bearer"}



