# -*- coding: utf-8
from .jwt_codec import decode_jwt


class PasswordAuthentication:
    """
    Password authentication
    """

    def __init__(self, user_query):
        self.user_query = user_query

    async def authenticate(self, email, password):
        # Reinitialize user_query instance
        user_query = self.user_query.new()

        # Get user by email
        user = await user_query.find_by_email(email=email).find()

        if user is None:
            return None

        # Validate password
        if user.check_password(password=password) is False:
            return None

        return user


class JwtAuthentication:
    """
    Jwt authentication
    """

    def __init__(self, user_query):
        self.user_query = user_query

    async def authenticate(self, token):
        # Reinitialize user_query instance
        user_query = self.user_query.new()

        # Decore jwt
        payload = decode_jwt(token=token)

        # Validate payload type
        if not payload.get('type', '') == 'authentication':
            return None

        user = await user_query.find_by_id(
            id=payload.get('user_id', None)).find()

        return user
