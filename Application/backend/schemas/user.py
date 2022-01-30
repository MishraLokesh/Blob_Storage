from pydantic import BaseModel
from typing import Optional

class Users(BaseModel):
  user_id: int
  email: str
  password: str

class Files(BaseModel):
  file_id: int
  file_name: str

class Relation(BaseModel):
  user_id: int
  file_id: int
  is_owner: int

class Login(BaseModel):
  username: str
  password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None