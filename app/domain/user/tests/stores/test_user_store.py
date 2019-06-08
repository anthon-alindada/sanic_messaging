# -*- coding: utf-8
# Core
import pytest

# Models
from app.domain.user.models import User

# User context
from ... import user_context


@pytest.fixture
def user_store():
    return user_context.user_store()


async def test_create(user_data, user_store):
    user = await user_store.create(
        email='email@cloud.com',
        first_name='anthon',
        last_name='alindada',
        password='password')

    assert user.id is not None, 'Should create user'
    assert isinstance(user, User), 'Should create user'


async def test_set_password(user_data, user_store):
    user = user_data[0]
    user = await user_store.set_password(user=user, password='password')
    await user_store.save()

    assert user.password is not None, 'Should set user password'


async def test_activate(user_data, user_store):
    inactive_user = None

    # Get first inactive user
    for user in user_data:
        if user.active is False:
            inactive_user = user

    assert inactive_user.active is False, 'Should get first inactive user'

    user = await user_store.activate(user=inactive_user)
    await user_store.save()

    assert user.active is True, 'Should mark user as active'
    assert user.email == inactive_user.email, 'Should mark user as active'
