# -*- coding: utf-8
# Core
from zxcvbn import zxcvbn
from sanic_wtf import SanicForm
from wtforms import StringField, validators, ValidationError


class SignupForm(SanicForm):
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

    _existing_user = None

    def set_existing_user(self, user):
        """
        Set existing user for email validation
        """
        self._existing_user = user

    def validate_email(self, email):
        if self._existing_user is not None:
            raise ValidationError('Email already exist')

        return email

    def validate_password(self, password):
        password_strength = zxcvbn(password.data)

        if password_strength.get('score') < 1:
            raise ValidationError('Password is too weak')

        return password
