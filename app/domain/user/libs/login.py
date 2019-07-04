# -*- coding: utf-8
# Core
from ..jwt_codec import generate_auth_jwt

# Exception
from ..exceptions import Unauthorized


class Login:
    """
    Login
    """

    def __init__(self, password_authentication, user_query):
        # Library
        self.password_authentication = password_authentication
        self.user_query = user_query

        # Errors
        self._errors = {}

    async def run(self, email, password):
        """
        Run the service
        """

        # Set user query active
        user_query_email = self.user_query.new()

        # Get user by email
        user = await user_query_email.filter_by_active(
            ).find_by_email(email).find()

        # If user is none
        if user is None:
            raise Unauthorized

        # Check password
        if user.check_password(password) is False:
            raise Unauthorized

        # Generate auth jwt
        jwt_token = generate_auth_jwt(
            user_id=user.id, email=user.email)

        return jwt_token
