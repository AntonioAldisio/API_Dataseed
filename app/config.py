import os
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

SECRET_KEY = os.getenv('SECRET_KEY', default='teste')
ALGORITHM = os.getenv('JWT_ALGORITHM', default='HS512')
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 # 1 dia

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)