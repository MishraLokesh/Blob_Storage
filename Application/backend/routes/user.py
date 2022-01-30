from fastapi import APIRouter
from sqlalchemy.sql import text
from schemas.user import Users
from schemas.user import Files
from schemas.user import Relation

from models.user import users
from models.user import files
from models.user import relations
 
from config.db import conn
user = APIRouter()


# fetch all users
@user.get('/')
async def fetch_users():
  return conn.execute(users.select()).fetchall()



# convert file to blob
def readfile(filename):
  with open(filename, "rb") as f:
      data = f.read()
  return data


def writefile(filename, data):
  with open(filename, "wb") as f:
      f.write(data)

#blob read from user file
# sample = readfile("img2.png")
 
# file created from blob data


# fetch user by id
@user.get('/{id}')
async def fetch_user_files(id: int):
  s1 = text("SELECT * FROM blob.files where file_id in (SELECT file_id FROM blob.relation where user_id = :userid)")
  blob_name = text("SELECT file_path FROM blob.files where file_id in (SELECT file_id FROM blob.relation where user_id = :userid)")
  s2 = text("SELECT file_name FROM blob.files where file_id in (SELECT file_id FROM blob.relation where user_id = :userid)")
  fileName = conn.execute(s2, userid=id).fetchall()[0][0]
  print(fileName)
  result = conn.execute(blob_name, userid=id).fetchall()
  writefile("Files_Download/"+fileName, result[0][0])

  return conn.execute(s1, userid=id).fetchall()


# insert new user
@user.post('/')
async def insert_user(user: Users, file: Files):
  fp = readfile("Files_Upload/"+file.file_name)
  conn.execute(users.insert().values(
    user_id=user.user_id,
    email=user.email,
    password=user.password
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
async def same_user_new_file(uid:int, file: Files):
  fp = readfile("Files_Upload/"+files.file_name)
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
  return conn.execute(users.select()).fetchall()

    
# update user
@user.put('/{id}')
async def update_user(id: int, user: Users, file: Files):
  conn.execute(users.update().values(
    user_id=user.user_id,
    email=user.email,
    password=user.password
  ).where(users.c.user_id == id))
  conn.execute(files.update().values(
    file_id=file.file_id,
    file_name=file.file_name,
    file_path=file.file_path,
  ).where(files.c.file_id == id))
  conn.execute(relations.update().values(
    user_id=user.user_id,
    file_id=file.file_id,
    is_owner=1,
  ).where(relations.c.user_id == id))
  return conn.execute(relations.select()).fetchall()
 

# give access to another user
@user.post('/{id1}')
async def access_to_new_user(id1: int, id2: int, fid: int):
  s = text("select is_owner from blob.relation where user_id = :userid")
  result1 = conn.execute(s, userid=id1).fetchall()
  print(result1)
  if(result1[0][0] == 1): 
    conn.execute(relations.insert().values(
      user_id=id2,
      file_id=fid,
      is_owner=0,
    ))
  return conn.execute(relations.select()).fetchall()


# delete user by id
@user.delete('/{id}')
async def delete_user(id: int):
  conn.execute(users.delete().where(users.c.user_id == id))
  conn.execute(files.delete().where(files.c.file_id == id))
  # conn.execute(relations.delete().where(relations.c.user_id == id))
  return conn.execute(users.select()).fetchall()

