# -*- coding: utf-8
# Models
from ..models import User


async def test_user_model(user_data):
    user = User(
        email='user@cloud.com',
        first_name='user',
        last_name='cloud')
    user.set_password('password')

    user = await user.create()

    assert repr(user) == "<User: 'user@cloud.com'>"

    # Validate password
    assert user.check_password('pass') is False, \
        'Should be an invalid password'

    assert user.check_password('password'), 'Should be a valid password'
