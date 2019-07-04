# -*- coding: utf-8
# Core
from zxcvbn import zxcvbn
from sanic_wtf import SanicForm
from wtforms import StringField, validators, ValidationError

# Exception
from ..exceptions import InvalidInput


class SignupValidator(SanicForm):
    """
    Signup form
    """

    first_name = StringField('First name', validators=[
        validators.DataRequired(
            message='First name is required',
        ),
        validators.Length(
            max=100,
            message='First name must be less than 100 characters',
        ),
    ])

    last_name = StringField('Last name', validators=[
        validators.DataRequired(
            message='Last name is required',
        ),
        validators.Length(
            max=100,
            message='Last name must be less than 100 characters',
        ),
    ])

    email = StringField('Email address', validators=[
        validators.DataRequired(
            message='Email address is required',
        ),
        validators.Email(
            message='Email address is invalid',
        ),
    ])

    password = StringField('Password', validators=[
        validators.DataRequired(
            message='Password is required',
        ),
        validators.Length(
            min=6,
            message='Password must have at least 6 characters',
        ),
        validators.Length(
            max=128,
            message='Password must be less than 128 characters',
        ),
    ])

    confirm_password = StringField('Confirm password', validators=[
        validators.DataRequired(
            message='Confirm password is required',
        ),
        validators.EqualTo(
            'password',
            message='Passwords don\'t match',
        ),
    ])

    def validate_password(self, password):
        password_strength = zxcvbn(password.data)

        if password_strength.get('score') < 1:
            raise ValidationError('Password is too weak')

        return password


class Signup:
    """
    Signup
    """

    def __init__(self, user_query, user_store):
        # Library
        self.user_query = user_query
        self.user_store = user_store

        # Errors
        self._errors = {}

    async def validate(
        self,
        first_name,
        last_name,
        email,
        password,
        confirm_password,
    ) -> bool:
        """
        Validate input data
        """

        # Validate signup form input
        signup_validator = SignupValidator(data={
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'confirm_password': confirm_password,
        })

        if signup_validator.validate() is False:
            # Set errors
            self._errors = signup_validator.errors

        # Check if email already exist
        if self._errors.get('email', None) is None:
            # Set user query active
            user_query_active = self.user_query.new()

            # Get active user with same email
            user = await user_query_active.filter_by_active(
                ).find_by_email(email).find()

            # If user exist
            if user is not None:
                await self.set_error('email', 'Email address already exist')

        # If errors exist
        if self._errors:
            return False

        return True

    async def set_error(self, field, message) -> None:
        """
        Set error field
        """
        self._errors[field] = [message]

    async def run(self, first_name, last_name, email,
                  password, confirm_password):
        """
        Run the service
        """

        # Validate input
        is_valid = await self.validate(
            first_name,
            last_name,
            email,
            password,
            confirm_password)

        if is_valid is False:
            raise InvalidInput(self._errors)

        # Set user query inactive
        user_query_inactive = self.user_query.new()

        # Get inactive user with same email
        user = await user_query_inactive.filter_by_inactive(
            ).find_by_email(email).find()

        if user is not None:
            # Delete existing inactive user
            await user.delete()

        # Create new inactive user
        user = await self.user_store.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password)

        # Activate user
        user = await self.user_store.activate(user=user)
        await self.user_store.save()

        return user

    async def get_errors(self):
        """
        Get errors
        """
        return self._errors
