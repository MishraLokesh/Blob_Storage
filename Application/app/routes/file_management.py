from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.user import Login
from sqlalchemy.sql import text
from config.db import conn
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from . import JWT_token
from lzma import compress
from fastapi import APIRouter, Depends
from sqlalchemy.sql import text
from schemas.user import Users
from schemas.user import Files
from schemas.user import Files_rename
from schemas.user import Relation

from models.user import users
from models.user import files
from models.user import relations
from config.db import conn
 
import zlib, sys, base64
from passlib.context import CryptContext
from . import oauth2


router = APIRouter(tags=['File Management'])

# convert blob to file
def writefile(filename, data):
  decompressed = zlib.decompress(base64.b64decode(data))
  with open(filename, "wb") as f:
    f.write(decompressed)


# fetch user by id
@router.post('/file/{id}')
async def download_user_file(id: int,f_id: int,current_user: Users = Depends(oauth2.get_current_user)):
  query = text("SELECT * FROM blob.relation where user_id = :uid and file_id = :fid;")
  file_exists = conn.execute(query, uid=id, fid=f_id).fetchall()
  if(file_exists):
    s1 = text("SELECT file_path FROM blob.files where file_id = :fileid")
    s2 = text("SELECT file_name FROM blob.files where file_id = :fileid")
    filePath = conn.execute(s1, fileid=f_id).fetchall()[0][0]
    fileName = conn.execute(s2, fileid=f_id).fetchall()[0][0]
    writefile("Files_Download/"+fileName, filePath)

  return "File successfully downloaded"


# rename file accessible to a user
@router.put('/file/{f_id}')
async def rename_user_file(f_id: int, u_id: int, file: Files_rename,current_user: Users = Depends(oauth2.get_current_user)):
  query1 = text("SELECT * FROM blob.relation where user_id=:uid and file_id = :fid and is_owner=1;")
  file_exists = conn.execute(query1, fid=f_id, uid=u_id).fetchall()
  print(file_exists)
  if(file_exists):
    s1 = text("SELECT file_path FROM blob.files where file_id = :fileid")
    filePath = conn.execute(s1, fileid=f_id).fetchall()[0][0]
    conn.execute(files.update().values(
      # file_id=f_id,
      file_name=file.file_name,
      # file_path=filePath,
    ).where(files.c.file_id == f_id))
  
  return "File successfully renamed"



# give access to another user
@router.post('/file/access/{id1}')
async def access_to_new_user(id1: int, id2: int, fid: int,current_user: Users = Depends(oauth2.get_current_user)):
  s = text("select is_owner from blob.relation where user_id = :userid and file_id=:fileid")
  result1 = conn.execute(s, userid=id1,fileid=fid).fetchall()
  print(result1)
  if(result1[0][0] == 1): 
    conn.execute(relations.insert().values(
      user_id=id2,
      file_id=fid,
      is_owner=0,
    ))
    return "File successfully shared"
  return "File could not be shared. You don't have the access to share this file"



# delete file by id
@router.delete('/file/{f_id}')
async def delete_user_file(f_id: int, u_id: int,current_user: Users = Depends(oauth2.get_current_user)):

  query1 = text("SELECT * FROM blob.relation where user_id=:uid and file_id = :fid and is_owner=1;")
  file_exists = conn.execute(query1, fid=f_id, uid=u_id).fetchall()
  print(file_exists)
  if(file_exists):
    conn.execute(files.delete().where(files.c.file_id == f_id))

  return "File successfully deleted"


