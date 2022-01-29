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


# fetch user by id
@user.get('/{id}')
async def fetch_user_files(id: int):
  s = text("SELECT * FROM blob.files where file_id in (SELECT file_id FROM blob.relation where user_id = :userid)")
  return conn.execute(s, userid=id).fetchall()


# insert new user
@user.post('/')
async def insert_user(user: Users, file: Files):
  conn.execute(users.insert().values(
    user_id=user.user_id,
    email=user.email,
    password=user.password
  ))
  conn.execute(files.insert().values(
    file_id=file.file_id,
    file_name=file.file_name,
    file_path=file.file_path,
  ))
  conn.execute(relations.insert().values(
    user_id=user.user_id,
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
async def access_to_new_user(id1: int, id2: int):
  s = text("select is_owner from blob.relation where user_id = :userid")
  result1 = conn.execute(s, userid=id1).fetchall()
  # print(result1)
  if(len(result1) > 0):
    conn.execute(relations.insert().values(
      user_id=id2,
      file_id=id1,
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

