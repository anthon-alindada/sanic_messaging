# -*- coding: utf-8
# Models
from ...models import User

# User context
from ... import user_context


async def test_find_user_by_id(user_data):
    user = await user_context.user_query().find_by_id(id=28239).find()
    assert user is None, 'Should return None if id does not exist'

    user = await user_context.user_query().find_by_id(id=1).find()
    assert isinstance(user, User), 'Should get user by id'


async def test_find_user_by_email(user_data):
    user = await user_context.user_query().find_by_email(email='asdf').find()
    assert user is None, 'Should return None if email does not exist'

    user = await user_context.user_query().find_by_email(
        email='test@cloud.com').find()
    assert isinstance(user, User), 'Should get user by email'


async def test_filter_user_by_active(user_data):
    users = await user_context.user_query().filter_by_active().filter()

    for user in users:
        assert user.active is True, 'Should filter all active users'


async def test_filter_user_by_inactive(user_data):
    users = await user_context.user_query().filter_by_inactive().filter()

    for user in users:
        assert user.active is False, 'Should filter all inactive users'
