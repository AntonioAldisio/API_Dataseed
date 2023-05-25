from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from public.schemas import TokenResponse
from private.schemas import messageResponse
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from utils.create_access_token import create_access_token
from utils.authenticate_user import authenticate_user
from database import get_db
from model.models import User


router = APIRouter(
    tags = ['Public'],
    responses = {404: {"description": "Not found"}},
)


@router.post("/register", response_model=messageResponse)
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


@router.put("/changePassword", response_model=messageResponse)
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


@router.post("/login", response_model=TokenResponse)
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


@router.post("/loginAuth", include_in_schema=False)
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
