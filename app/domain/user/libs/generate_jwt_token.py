# -*- coding: utf-8
# Core
from ..jwt_codec import generate_auth_jwt


class GenerateJwtToken:
    """
    Generate jwt token
    """

    def __init__(self):
        pass

    async def run(self, user):
        """
        Run the service
        """

        # Generate auth jwt
        jwt_token = generate_auth_jwt(
            user_id=user.id, email=user.email)

        return jwt_token
