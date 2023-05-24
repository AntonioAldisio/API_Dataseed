from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "mysql+pymysql://root:mysecretpw@0.0.0.0:3306/db"

engine = create_engine(
    DATABASE_URL,
    pool_size=200,
    max_overflow=0
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db(expire_on_commit: bool = True):
    db = SessionLocal(expire_on_commit=expire_on_commit)
    try:
        return db
    finally:
        db.close()
