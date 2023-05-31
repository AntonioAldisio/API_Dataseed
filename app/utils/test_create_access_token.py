from datetime import timedelta
from .create_access_token import create_access_token


def test_create_access_token():
    # Arrange
    data = {"user_id": 1}
    expires_delta = timedelta(minutes=30)

    # Act
    token = create_access_token(data, expires_delta)

    # Assert
    assert isinstance(token, str)
    assert len(token) > 0
