from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    username = Column(String(50), nullable=False)
    nome = Column(String(100), nullable=False)
    email = Column(String(50), primary_key=True)
    password = Column(String(50), nullable=False)
    status = Column(Boolean, nullable=False)
