from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine


users = Table ('users', meta, 
Column('user_id', Integer, primary_key=True),
Column('email', String(255)),
Column('password', String(255)),
)

files = Table ('files', meta, 
Column('file_id', Integer, primary_key=True),
Column('file_name', String(255)),
Column('file_path', String(255)),
)

relations = Table ('relation', meta, 
Column('user_id', Integer, primary_key=True),
Column('file_id', Integer),
Column('is_owner', Integer),
)


meta.create_all(engine)
