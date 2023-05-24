from fastapi import FastAPI, Depends, HTTPException, Request, Header
from sqlalchemy.orm import Session
from database import get_db
from model.models import User
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional
import jwt
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/loginAuth")

@app.get("/")
async def index():
    return {"status": "ok"}

# Rota de cadastro
@app.post("/cadastro")
async def cadastrar_usuario(username: str,
                      nome: str,
                      email: str,
                      password: str,
                      status: bool,
                      db: Session = Depends(get_db)):
    user = User(username=username, nome=nome, email=email, password=password, status=status)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Usuário cadastrado com sucesso"}

# Rota para trocar a senha
@app.put("/trocar-senha")
async def trocar_senha(email: str,
                 senha_atual: str,
                 nova_senha: str,
                 db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if user.password != senha_atual:
        raise HTTPException(status_code=400, detail="Senha atual incorreta")

    user.password = nova_senha
    db.commit()

    return {"message": "Senha atualizada com sucesso"}


# Função para gerar o JWT token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if user.password != password:
        return False
    return True

@app.post("/login")
async def login(username: str, password: str, db: Session = Depends(get_db)):
    email = username
    senha = password

    if not authenticate_user(email, senha, db=db):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # Generate JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/loginAuth", include_in_schema=False)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    email = form_data.username
    senha = form_data.password

    if not authenticate_user(email, senha, db=db):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # Gera o token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# Função para obter os dados do usuário atualmente autenticado
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

# Rota para obter as informações do usuário autenticado
@app.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {
        "login": current_user.username,
        "nome": current_user.nome,
        "email": current_user.email,
        "status": current_user.status
    }



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)