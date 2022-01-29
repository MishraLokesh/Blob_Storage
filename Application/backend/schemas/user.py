from pydantic import BaseModel

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
  