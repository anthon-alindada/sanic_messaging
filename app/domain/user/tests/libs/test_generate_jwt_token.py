# -*- coding: utf-8
# Core
import pytest

# Query set
from app.domain.user.query_sets.user_query import UserQuery

# User context
from ... import user_context


@pytest.fixture
def generate_jwt_token_lib():
    return user_context.generate_jwt_token()


async def test_activate_account(generate_jwt_token_lib, user_data):
    user_instance = await UserQuery().find_by_id(id=user_data[0].id).find()

    jwt_token = await generate_jwt_token_lib.run(user=user_instance)

    assert jwt_token is not None, 'Should generate jwt token'
