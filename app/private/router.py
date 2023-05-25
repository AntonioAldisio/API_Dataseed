
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from private.schemas import UserInfoResponse, messageResponse
from utils.get_current_user import get_current_user
from database import get_db
from model.models import User
from typing import Optional



router = APIRouter(
    tags = ['Private'],
    responses = {404: {"description": "Not found"}},
)

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
def delete_current_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.delete(current_user)
    db.commit()
    return {"message": "Usuário deletado com sucesso"}