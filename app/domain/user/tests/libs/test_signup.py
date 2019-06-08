# -*- coding: utf-8
# Core
import pytest

# Models
from app.domain.user.models import User

# Exception
from app.domain.user.exceptions import InvalidInput

# User context
from ... import user_context


@pytest.fixture
def signup_lib():
    return user_context.signup()


async def test_signup_invalid_form(user_data, signup_lib):
    errors = None
    try:
        await signup_lib.run(
            first_name='',
            last_name='',
            email='',
            password='',
            confirm_password='')
    except InvalidInput:
        errors = await signup_lib.get_errors()

    assert errors is not None, 'Should fail if form has an error'


async def test_signup_existing_inactive_user(user_data, signup_lib):
    user = await signup_lib.run(
        first_name='Anthon',
        last_name='Alindada',
        email='inactive@cloud.com',
        password='passwordinactive',
        confirm_password='passwordinactive')

    assert isinstance(user, User), 'Should create inactive user'
    assert user.active is True, 'Should create inactive user'


async def test_signup(user_data, signup_lib):
    user = await signup_lib.run(
        first_name='Anthon',
        last_name='Alindada',
        email='anthon.alindada.435@gmail.com',
        password='anthonpasswordinactive',
        confirm_password='anthonpasswordinactive')

    assert isinstance(user, User), 'Should create inactive user'
    assert user.active is True, 'Should create inactive user'
