# -*- coding: utf-8
# Core
import pytest

# Store
from app.domain.user.stores.user_store import UserStore

# Exception
from app.domain.user.exceptions import Unauthorized

# User context
from ... import user_context


@pytest.fixture
def login_lib():
    return user_context.login()


@pytest.fixture
def user_query():
    return user_context.user_query()


async def test_login_inactive_user(user_data, user_query, login_lib):
    # Get inactive user
    users = await user_query.filter_by_inactive().filter()

    # Set user data and password
    user_instance = users[0]
    user_store = UserStore()
    user_instance = await user_store.set_password(
        user=user_instance, password='testpassword')

    # Login
    is_login_failed = None

    try:
        await login_lib.run(
            email=user_instance.email, password='testpassword')
    except Unauthorized:
        is_login_failed = True

    assert is_login_failed is True, \
        'Should fail login if account is inactive'


async def test_login_invalid_email(user_data, login_lib):
    # Login
    is_login_failed = None

    try:
        await login_lib.run(
            email='doesnotexist@email.com', password='testpassword')
    except Unauthorized:
        is_login_failed = True

    assert is_login_failed is True, \
        'Should fail login if email does not exist'


async def test_login_invalid_password(user_data, user_query, login_lib):
    # Get inactive user
    users = await user_query.filter_by_active().filter()

    # Set user data and password
    user_instance = users[0]
    user_store = UserStore()
    user_instance = await user_store.set_password(
        user=user_instance, password='testpassword')
    await user_store.save()

    # Login
    is_login_failed = None

    try:
        await login_lib.run(
            email=user_instance.email, password='invalidpassword')
    except Unauthorized:
        is_login_failed = True

    assert is_login_failed is True, \
        'Should fail login if password is invalid'


async def test_login(user_data, user_query, login_lib):
    # Get inactive user
    users = await user_query.filter_by_active().filter()

    # Set user data and password
    user_instance = users[0]
    user_store = UserStore()
    user_instance = await user_store.set_password(
        user=user_instance, password='testpassword')
    await user_store.save()

    # Login
    jwt_token = await login_lib.run(
        email=user_instance.email, password='testpassword')

    assert jwt_token, 'Should login if email and password is valid'
