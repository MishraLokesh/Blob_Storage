from sqlalchemy import create_engine, MetaData
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "mysql://localhost:3306/blob"

engine = create_engine(
    'mysql+pymysql://root:password@localhost:3306/blob'
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

meta = MetaData()
conn = engine.connect()
