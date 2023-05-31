from sqlalchemy.orm import Session
from unittest import mock
from .authenticate_user import authenticate_user
from model.models import User


def test_authenticate_user_with_valid_credentials():
    username = "testuser"
    password = "testpassword"
    user = User(username=username, password=password)
    db = mock.Mock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = user

    result = authenticate_user(username, password, db=db)

    assert result is True


def test_authenticate_user_with_invalid_credentials():
    # Arrange
    username = "testuser"
    password = "testpassword"
    db = mock.Mock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = None

    # Act
    result = authenticate_user(username, password, db=db)

    # Assert
    assert result is False
