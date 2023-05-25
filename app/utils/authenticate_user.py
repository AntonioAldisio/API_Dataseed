from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from model.models import User


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if user.password != password:
        return False
    return True