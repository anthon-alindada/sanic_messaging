# -*- coding: utf-8
# Core
import pytest
from app.domain.user.jwt_codec import generate_auth_jwt

# Models
from app.domain.user.models import User

# Store
from app.domain.user.stores.user_store import UserStore

# User context
from .. import user_context


@pytest.fixture
def password_authentication():
    return user_context.password_authentication()


@pytest.fixture
def jwt_authentication():
    return user_context.jwt_authentication()


async def test_password_authentication_valid(
    user_data,
    password_authentication
):
    # Set user data and password
    user_instance = user_data[0]
    user_store = UserStore()
    user_instance = await user_store.set_password(
        user=user_instance, password='testpassword')
    await user_store.save()

    # Authenticate
    user = await password_authentication.authenticate(
        email=user_instance.email, password='testpassword')
    assert isinstance(user, User), \
        'Should return user instance if email and password is correct'


async def test_password_authentication_invalid_email(
    user_data,
    password_authentication
):
    # Authenticate
    user = await password_authentication.authenticate(
        email='wrong@email.com', password='testpassword')
    assert user is None, 'Should return none if email does not exist'


async def test_password_authentication_invalid_rassword(
    user_data,
    password_authentication
):
    # Set user data and password
    user_instance = user_data[0]

    # Authenticate
    user = await password_authentication.authenticate(
        email=user_instance.email, password='wrongpassword')
    assert user is None, 'Should return none if password is incorrect'


async def test_jwt_authentication_valid(user_data, jwt_authentication):
    user = user_data[0]
    token = generate_auth_jwt(user.id, user.email)

    # Authenticate
    user = await jwt_authentication.authenticate(token=token)
    assert isinstance(user, User), \
        'Should return user instance if token is correct'


async def test_jwt_authentication_invalid_token(user_data, jwt_authentication):
    # Set token
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9'

    # Authenticate
    user = await jwt_authentication.authenticate(token=token)
    assert user is None, 'Should return None if token is incorrect'


async def test_jwt_authentication_expired_token(user_data, jwt_authentication):
    # Set token
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYXV0aGVudGljYXRpb24iLCJ1c2VyX2lkIjoxLCJlbWFpbCI6InRlc3RAY2xvdWQuY29tIiwiZXhwIjoxNTMxMDU3NjExfQ.NUzsWxCA1FhlT07JVI0pSZVLqEG1kQvXrgmSlAybFRc'  # noqa

    # Authenticate
    user = await jwt_authentication.authenticate(token=token)
    assert user is None, 'Should return None if token is expired'
