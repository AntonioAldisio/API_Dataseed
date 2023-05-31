import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from unittest import mock
from .get_current_user import get_current_user
from model.models import User
import jwt


def test_get_current_user_with_valid_token():
    token = "valid_token"
    username = "testuser"
    user = User(username=username)
    db = mock.Mock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = user
    jwt.decode = mock.Mock(return_value={"sub": username})

    result = get_current_user(token, db=db)

    assert result == user


def test_get_current_user_with_invalid_token():
    token = "invalid_token"
    db = mock.Mock(spec=Session)
    jwt.decode = mock.Mock(side_effect=jwt.ExpiredSignatureError)

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token, db=db)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Token expirado"


def test_get_current_user_with_missing_username():
    token = "valid_token"
    db = mock.Mock(spec=Session)
    jwt.decode = mock.Mock(return_value={})

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token, db=db)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail != "Usuário não encontrado"
