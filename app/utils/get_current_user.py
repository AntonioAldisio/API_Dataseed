from fastapi.security import OAuth2PasswordBearer
from config import ALGORITHM, SECRET_KEY
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from model.models import User
from database import get_db
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/loginAuth")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        user = db.query(User).filter(User.username == username).first()
        if username is None:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")