# -*- coding: utf-8
# Core
import pytest

# User context
from ... import user_context


@pytest.fixture
def user_query():
    return user_context.user_query()


async def test_signup_form_email(user_data, user_query):
    # Validate blank email
    signup_form = user_context.signup_form()(data={'email': ''})

    signup_form.validate()

    assert signup_form.errors.get('email') == ['Email address is required'], \
        'Should be invalid if email is blank'

    # Validate invalid email
    signup_form = user_context.signup_form()(data={
        'email': 'invalid',
    })

    signup_form.validate()

    assert signup_form.errors.get('email') == ['Email address is invalid'], \
        'Should be invalid if email is invalid'

    # Validate existing email
    email = 'test@cloud.com'
    user = await user_query.find_by_email(email).find()
    signup_form = user_context.signup_form()(data={
        'email': email,
    })

    # Set existing user with email
    signup_form.set_existing_user(user=user)

    signup_form.validate()

    assert signup_form.errors.get('email') == ['Email already exist'], \
        'Should be invalid if email already exist'

    # Validate correct email
    signup_form = user_context.signup_form()(data={
        'email': 'email@cloud.com',
    })

    signup_form.validate()

    assert signup_form.errors.get('email') is None, 'Should be a valid email'


async def test_signup_form_first_name(user_data):
    # Validate blank first name
    signup_form = user_context.signup_form()(data={
        'first_name': '',
    })

    signup_form.validate()

    assert signup_form.errors.get('first_name') == \
        ['First name is required'], 'Should be invalid if first name is blank'

    # Validate length first name
    signup_form = user_context.signup_form()(data={
        'first_name': 'aasdfjklsadjflksdajflsdajfklsadasdfjklsadjflksdajflsdajfklsadasdfjklsadjflksdajflsdajfklsadsdfjklsadjflksdajflsdajfklsad',  # noqa
    })

    signup_form.validate()

    assert signup_form.errors.get('first_name') == \
        ['First name must be less than 100 characters'], \
        'Should be invalid if first name is more than 100 characters'

    # Validate correct first name
    signup_form = user_context.signup_form()(data={
        'first_name': 'first',
    })

    signup_form.validate()

    assert signup_form.errors.get('first_name') is None, \
        'Should be a valid first name'


async def test_signup_form_last_name(user_data):
    # Validate blank last name
    signup_form = user_context.signup_form()(data={
        'last_name': '',
    })

    signup_form.validate()

    assert signup_form.errors.get('last_name') == \
        ['Last name is required'], 'Should be invalid if last name is blank'

    # Validate length last name
    signup_form = user_context.signup_form()(data={
        'last_name': 'aasdfjklsadjflksdajflsdajfklsadasdfjklsadjflksdajflsdajfklsadasdfjklsadjflksdajflsdajfklsadsdfjklsadjflksdajflsdajfklsad',  # noqa
    })

    signup_form.validate()

    assert signup_form.errors.get('last_name') == \
        ['Last name must be less than 100 characters'], \
        'Should be invalid if last name is more than 100 characters'

    # Validate correct last name
    signup_form = user_context.signup_form()(data={
        'last_name': 'last',
    })

    signup_form.validate()

    assert signup_form.errors.get('last_name') is None, \
        'Should be a valid last name'


async def test_signup_form_password(user_data):
    # Validate blank password
    signup_form = user_context.signup_form()(data={
        'password': '',
    })

    signup_form.validate()

    assert signup_form.errors.get('password') == ['Password is required'], \
        'Should be invalid if password is blank'

    # Validate max length password
    signup_form = user_context.signup_form()(data={
        'password': 'aasdfjklsadjflksdajflsdajfklsadasdfjklsadjflksdajflsdajfklsadasdfjklsadjflksdajflsdajfklsadsdfjklsadjflksdajflsdajfklsadahsdfjhuihdsafkjhsdauifsadfksndfqweuihd',  # noqa
    })

    signup_form.validate()

    assert signup_form.errors.get('password') == \
        ['Password must be less than 128 characters'], \
        'Should be invalid if password is more than 128'

    # Validate min length password
    signup_form = user_context.signup_form()(data={
        'password': '1234',
    })

    signup_form.validate()

    assert 'Password must have at least 6 characters' in \
        signup_form.errors.get('password'), \
        'Should be invalid if password is less than 6'

    # Validate password strength
    signup_form = user_context.signup_form()(data={
        'password': 'password123',
    })

    signup_form.validate()

    assert 'Password is too weak' in signup_form.errors.get('password'), \
        'Should be invalid if password is too weak'

    # Validate correct password
    signup_form = user_context.signup_form()(data={
        'password': 'password1234',
    })

    signup_form.validate()

    assert signup_form.errors.get('password') is None, \
        'Should be a valid password'


async def test_signup_form_confirm_password(user_data):
    # Validate blank confirm password
    signup_form = user_context.signup_form()(data={
        'confirm_password': '',
    })

    signup_form.validate()

    assert signup_form.errors.get('confirm_password') == \
        ['Confirm password is required'], \
        'Should be invalid if confirm password is blank'

    # Validate blank confirm password dont match
    signup_form = user_context.signup_form()(data={
        'password': 'password',
        'confirm_password': 'password123',
    })

    signup_form.validate()

    assert signup_form.errors.get('confirm_password') == \
        ['Passwords don\'t match'], \
        'Should be invalid if confirm password is dont match'

    # Validate correct confirm password
    signup_form = user_context.signup_form()(data={
        'password': 'password1234',
        'confirm_password': 'password1234',
    })

    signup_form.validate()

    assert signup_form.errors.get('confirm_password') is None, \
        'Should be a valid confirm password'
