# -*- coding: utf-8
# Core
from functools import wraps
from graphql import GraphQLError

# Contexts
from app.domain.user import user_context
from .. import app


def csrf(f):
    """
    Validate csrf token header and cookie if matched
    """

    @wraps(f)
    async def decorated_function(self, info, *args, **kwargs):
        # Disable csrf if development
        if app.config.get('APP_CONFIG') == 'development':
            return await f(self, info, *args, **kwargs)

        request = info.context.get('request')

        # If request method is POST
        # Validate csrf
        csrf_token_cookie = request.cookies.get('t', None)
        csrf_token_input = request.headers.get(
            'x-csrf-token', None) or request.form.get(
                'csrf_token', None)

        # If csrf header or cookies are either None
        if csrf_token_cookie is None or csrf_token_input is None:
            raise GraphQLError(message='Forbidden')

        # If csrf tokens are mismatched
        if csrf_token_cookie != csrf_token_input:
            raise GraphQLError(message='Forbidden')

        # If csrf is valid
        response = await f(self, info, *args, **kwargs)
        return response

    return decorated_function


def auth_required(f):
    """
    Validate authentications
    Jwt authentication
    """

    @wraps(f)
    async def decorated_function(self, info, *args, **kwargs):
        request = info.context.get('request')
        jwt_token = request.cookies.get('jwt_token', '')

        # Validate jwt token
        user = await user_context.jwt_authentication().authenticate(
            token=jwt_token)

        # If user does not exist
        # Return unauthorized
        if user is None:
            raise GraphQLError(message='Unauthorized')

        # Set user
        info.context['user'] = user
        response = await f(self, info, *args, **kwargs)
        return response

    return decorated_function
