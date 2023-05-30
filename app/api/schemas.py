from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserInfoResponse(BaseModel):
    login: str
    nome: str
    email: str
    status: bool


class messageResponse(BaseModel):
    message: str
