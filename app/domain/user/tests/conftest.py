# -*- coding: utf-8
# Core
import pytest
from datetime import datetime
from mixer.main import mixer

# App
from app import create_app


app = create_app('test')


class UserFactory:
    id = int
    email = str
    first_name = str
    last_name = str
    active = bool
    date_joined = datetime


@pytest.fixture
def sanic_server(loop, test_server):
    return loop.run_until_complete(test_server(app))


def pytest_namespace():
    return {
        'users_data': None,
    }


@pytest.fixture
def user_data(loop, sanic_server, request):
    """
    Initial user domain test
    """
    # Models
    from ..models import User

    if pytest.users_data is None:
        # Delete all users data in database
        loop.run_until_complete(User.delete.gino.status())

        users_data = []

        # Generate fixed active user
        user_instance = loop.run_until_complete(User.create(
            id=1,
            email='test@cloud.com',
            first_name='first',
            last_name='last',
            active=True))

        users_data.append(user_instance)

        # Generate fix inactive user
        user_instance = loop.run_until_complete(User.create(
            email='inactive@cloud.com',
            first_name='inactive',
            last_name='account',
            active=False))

        users_data.append(user_instance)

        # Generate random users
        users = mixer.cycle(10).blend(UserFactory)

        for user in users:
            user_instance = loop.run_until_complete(User.create(
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                active=user.active,
                date_joined=user.date_joined))

            users_data.append(user_instance)

        pytest.users_data = users_data

    return pytest.users_data
