from lzma import compress
from fastapi import APIRouter, Depends
from sqlalchemy.sql import text
from schemas.user import Users
from schemas.user import Files
from schemas.user import Relation

from models.user import users
from models.user import files
from models.user import relations
from config.db import conn
 
import zlib, sys, base64
from passlib.context import CryptContext
from . import oauth2

user = APIRouter(tags=['User management'])


# fetch all users
@user.get('/')
async def fetch_users(current_user: Users = Depends(oauth2.get_current_user)):
  return conn.execute(users.select()).fetchall()


# convert file to blob
def readfile(filename):
  with open(filename, "rb") as f:
    data = f.read()
  # print ('Raw size: ',sys.getsizeof(data), '\n') 
  compressed = base64.b64encode(zlib.compress(data, 9))
  # print ('Compressed size: ',sys.getsizeof(compressed)) 
  return compressed


# convert blob to file
def writefile(filename, data):
  decompressed = zlib.decompress(base64.b64decode(data))
  with open(filename, "wb") as f:
    f.write(decompressed)



# fetch user by id
@user.get('/{id}')
async def fetch_user_files(id: int,current_user: Users = Depends(oauth2.get_current_user)):
  s1 = text("SELECT file_id, file_name FROM blob.files where file_id in (SELECT file_id FROM blob.relation where user_id = :userid)")
  result = conn.execute(s1, userid=id).fetchall()
  return result


# insert new user
@user.post('/')
async def insert_user(user: Users, file: Files,current_user: Users = Depends(oauth2.get_current_user)):
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  hashed_pass = pwd_context.hash(user.password)

  fp = readfile("Files_Upload/"+file.file_name)
  conn.execute(users.insert().values(
    user_id=user.user_id,
    email=user.email,
    password=hashed_pass
  ))
  conn.execute(files.insert().values(
    file_id=file.file_id,
    file_name=file.file_name,
    file_path=fp,
  ))
  conn.execute(relations.insert().values(
    user_id=user.user_id,
    file_id=file.file_id,
    is_owner=1,
  ))
  return conn.execute(users.select()).fetchall()


# insert new file for same user
@user.post('/{id}')
async def same_user_new_file(uid:int, file: Files,current_user: Users = Depends(oauth2.get_current_user)):
  fp = readfile("Files_Upload/"+file.file_name)
  conn.execute(files.insert().values(
    file_id=file.file_id,
    file_name=file.file_name,
    file_path=fp,
  ))
  conn.execute(relations.insert().values(
    user_id=uid,
    file_id=file.file_id,
    is_owner=1,
  ))
  return "New file successfully inserted"


# update user
@user.put('/{id}')
async def update_user(id: int, user: Users,current_user: Users = Depends(oauth2.get_current_user)):
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  hashed_pass = pwd_context.hash(user.password)
  conn.execute(users.update().values(
    user_id=user.user_id,
    email=user.email,
    password=hashed_pass
  ).where(users.c.user_id == id))
  return "User details successfully updated"
 

# delete user by id
@user.delete('/{id}')
async def delete_user(id: int,current_user: Users = Depends(oauth2.get_current_user)):
  conn.execute(users.delete().where(users.c.user_id == id))
  # conn.execute(relations.delete().where(relations.c.user_id == id))
  return "User successfully deleted"

