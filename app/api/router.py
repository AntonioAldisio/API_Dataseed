from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from api.schemas import TokenResponse, UserInfoResponse, messageResponse
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from utils.create_access_token import create_access_token
from utils.authenticate_user import authenticate_user
from database import get_db
from model.models import User

from utils.get_current_user import get_current_user
from database import get_db
from model.models import User
from typing import Optional


router = APIRouter(
    tags=['API'],
    responses={404: {"description": "Not found"}},
)


@router.get("/", include_in_schema=False)
async def index():
    return {"status": "ok"}


@router.post("/register", response_model=messageResponse)
async def cadastrar_usuario(username: str,
                            nome: str,
                            email: str,
                            password: str,
                            status: bool,
                            db: Session = Depends(get_db)):
    user = User(username=username,
                nome=nome,
                email=email,
                password=password,
                status=status)
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
        raise HTTPException(status_code=404,
                            detail="Usuário não encontrado")

    if user.password != senha_atual:
        raise HTTPException(status_code=400,
                            detail="Senha atual incorreta")

    user.password = nova_senha
    db.commit()

    return {"message": "Senha atualizada com sucesso"}


@router.post("/login", response_model=TokenResponse)
async def login(username: str,
                password: str,
                db: Session = Depends(get_db)):
    email = username
    senha = password

    if not authenticate_user(email, senha, db=db):
        raise HTTPException(status_code=401,
                            detail="Credenciais inválidas")

    # Generate JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/loginAuth", include_in_schema=False)
async def login_auth(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    email = form_data.username
    senha = form_data.password

    if not authenticate_user(email, senha, db=db):
        raise HTTPException(status_code=401,
                            detail="Credenciais inválidas")

    # Gera o token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/user", response_model=UserInfoResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {
        "login": current_user.username,
        "nome": current_user.nome,
        "email": current_user.email,
        "status": current_user.status
    }


@router.put("/updateUser", response_model=messageResponse)
async def update_current_user_info(
    username: Optional[str] = None,
    nome: Optional[str] = None,
    email: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Atualize os campos do usuário com base nos dados fornecidos
    if username:
        current_user.username = username
    if nome:
        current_user.nome = nome
    if email:
        current_user.email = email
    if status is not None:
        current_user.status = status

    # Commit as alterações no banco de dados
    db.commit()

    return {"message": "Usuário atualizado com sucesso"}


@router.delete("/deleteUser", response_model=messageResponse)
def delete_current_user(current_user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    db.delete(current_user)
    db.commit()
    return {"message": "Usuário deletado com sucesso"}
