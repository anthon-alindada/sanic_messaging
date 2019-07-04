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


async def test_signup_email_input(user_data, signup_lib):
    """
    Signup test email input
    """
    errors = None

    # Test if email is blank
    try:
        await signup_lib.run(
            first_name='',
            last_name='',
            email='',
            password='',
            confirm_password='')
    except InvalidInput:
        errors = await signup_lib.get_errors()

    assert errors.get('email') == ['Email address is required'], \
        'Should fail if email is blank'

    # Test if email is invalid
    try:
        await signup_lib.run(
            first_name='',
            last_name='',
            email='invalid',
            password='',
            confirm_password='')
    except InvalidInput:
        errors = await signup_lib.get_errors()

    assert errors.get('email') == ['Email address is invalid'], \
        'Should fail email is invalid'

    # Test if email already exist
    try:
        await signup_lib.run(
            first_name='',
            last_name='',
            email='test@cloud.com',
            password='',
            confirm_password='')
    except InvalidInput:
        errors = await signup_lib.get_errors()

    assert errors.get('email') == ['Email address already exist'], \
        'Should fail email already exist'

    # Test if email is valid
    try:
        await signup_lib.run(
            first_name='',
            last_name='',
            email='valid@cloud.com',
            password='',
            confirm_password='')
    except InvalidInput:
        errors = await signup_lib.get_errors()

    assert errors.get('email') is None, 'Should be a valid email'


async def test_signup_first_name_input(user_data, signup_lib):
    """
    Signup test first name input
    """
    errors = None

    # Test if first_name is blank
    try:
        await signup_lib.run(
            first_name='',
            last_name='',
            email='',
            password='',
            confirm_password='')
    except InvalidInput:
        errors = await signup_lib.get_errors()

    assert errors.get('first_name') == ['First name is required'], \
        'Should fail if first_name is blank'

    # Test if first_name morethan 100
    try:
        await signup_lib.run(
            first_name='jsadkfjasdlkfjaslkdjflaksdjflkasdjfksdjsadkfjasdlkfjaslkdjflaksdjflkasdjfksdjsadkfjasdlkfjaslkdjflaksdjflkasdjfksd',  # noqa
            last_name='',
            email='',
            password='',
            confirm_password='')
    except InvalidInput:
        errors = await signup_lib.get_errors()

    assert errors.get(
        'first_name') == ['First name must be less than 100 characters'], \
        'Should fail if first_name is morethan 100 characters'

    # Test if first_name is valid
    try:
        await signup_lib.run(
            first_name='anthon',
            last_name='',
            email='',
            password='',
            confirm_password='')
    except InvalidInput:
        errors = await signup_lib.get_errors()

    assert errors.get('first_name') is None, 'Should be a valid first name'


async def test_signup_last_name_input(user_data, signup_lib):
    """
    Signup test last name input
    """
    errors = None

    # Test if last_name is blank
    try:
        await signup_lib.run(
            first_name='',
            last_name='',
            email='',
            password='',
            confirm_password='')
    except InvalidInput:
        errors = await signup_lib.get_errors()

    assert errors.get('last_name') == ['Last name is required'], \
        'Should fail if last_name is blank'

    # Test if last_name morethan 100
    try:
        await signup_lib.run(
            last_name='jsadkfjasdlkfjaslkdjflaksdjflkasdjfksdjsadkfjasdlkfjaslkdjflaksdjflkasdjfksdjsadkfjasdlkfjaslkdjflaksdjflkasdjfksd',  # noqa
            first_name='',
            email='',
            password='',
            confirm_password='')
    except InvalidInput:
        errors = await signup_lib.get_errors()

    assert errors.get(
        'last_name') == ['Last name must be less than 100 characters'], \
        'Should fail if last_name is morethan 100 characters'

    # Test if last_name is valid
    try:
        await signup_lib.run(
            first_name='',
            last_name='alindada',
            email='',
            password='',
            confirm_password='')
    except InvalidInput:
        errors = await signup_lib.get_errors()

    assert errors.get('last_name') is None, 'Should be a valid last name'


async def test_signup_password_input(user_data, signup_lib):
    """
    Signup test password input
    """
    errors = None

    # Test if password is blank
    try:
        await signup_lib.run(
            first_name='',
            last_name='',
            email='',
            password='',
            confirm_password='')
    except InvalidInput:
        errors = await signup_lib.get_errors()

    assert errors.get('password') == ['Password is required'], \
        'Should fail if password is blank'

    # Test if password is morethan 128 characters
    try:
        await signup_lib.run(
            first_name='',
            last_name='',
            email='',
            password='aaasjdfkljsadfklasjdfkljsadfklasjdfkljsadfklasjdfkljsadfklasjdfkljsadfklsjdfkljsadfklasjdfkljsadfklasjdfkljsadfklasjdfkljsadfklasjdfkljsadfklasjdfkljsadfklsjdfkljsadfkl',  # noqa
            confirm_password='')
    except InvalidInput:
        errors = await signup_lib.get_errors()

    assert errors.get(
        'password') == ['Password must be less than 128 characters'], \
        'Should be invalid if password is more than 128'

    # Test if password is weak
    try:
        await signup_lib.run(
            first_name='',
            last_name='',
            email='',
            password='1234567',  # noqa
            confirm_password='')
    except InvalidInput:
        errors = await signup_lib.get_errors()

    assert errors.get(
        'password') == ['Password is too weak'], \
        'Should be invalid if password is too weak'

    # Test if password is valid
    try:
        await signup_lib.run(
            first_name='',
            last_name='',
            email='',
            password='a_UB5A_+q(',  # noqa
            confirm_password='')
    except InvalidInput:
        errors = await signup_lib.get_errors()

    assert errors.get('password') is None, 'Should be a valid password'


async def test_signup_confirm_password_input(user_data, signup_lib):
    """
    Signup test confirm password input
    """
    errors = None

    # Test if confirm password is blank
    try:
        await signup_lib.run(
            first_name='',
            last_name='',
            email='',
            password='',
            confirm_password='')
    except InvalidInput:
        errors = await signup_lib.get_errors()

    assert errors.get(
        'confirm_password') == ['Confirm password is required'], \
        'Should fail if confirm password is blank'

    # Test if confirm password does not match with password
    try:
        await signup_lib.run(
            first_name='',
            last_name='',
            email='',
            password='password1234',
            confirm_password='passworddoesnotmatch')
    except InvalidInput:
        errors = await signup_lib.get_errors()

    assert errors.get(
        'confirm_password') == ['Passwords don\'t match'], \
        'Should be invalid if confirm password is dont match'

    # Test if confirm password is valid
    try:
        await signup_lib.run(
            first_name='',
            last_name='',
            email='',
            password='password1234',
            confirm_password='password1234')
    except InvalidInput:
        errors = await signup_lib.get_errors()

    assert errors.get('confirm_password') is None, \
        'Should be a valid confirm password'


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
