# -*- coding: utf-8
from sanic import Blueprint
from sanic.response import redirect
from .. import jinja
from ..api_response import ApiResponse

# Exception
from app.domain.user.exceptions import Unauthorized

# Decorator
from ..decorators import csrf, guest_only, auth_required

# Contexts
from app.domain.user import user_context

# Helpers
from ..helpers import set_jwt_token_cookie


auth_views = Blueprint('auth', __name__)


@auth_views.route('/login', methods=['GET'])
@jinja.template('login/login.html')
@guest_only()
async def login(request):
    return {}


@auth_views.route('/api/login', methods=['POST'])
@csrf()
@guest_only()
async def api_login(request):
    if request.method == 'POST':
        # Login lib
        login_lib = user_context.login()

        try:
            jwt_token = await login_lib.run(
                email=request.json.get('email', ''),
                password=request.json.get('password', ''))

            # Return jwt token
            response = ApiResponse().success(data=jwt_token)

            # Set jwt cookie
            await set_jwt_token_cookie(response, jwt_token)

            return response
        except Unauthorized:
            return ApiResponse().unauthorized(
                message='Incorrect email or password')


@auth_views.route('/logout', methods=['GET'])
async def logout(request):
    # Return redirect to activation
    response = redirect('/login')

    # Set jwt cookie
    del response.cookies['jwt_token']
    del response.cookies['jwt_expiration']

    return response


@auth_views.route('/refresh_token', methods=['POST'])
@csrf()
@auth_required()
async def refresh_token(request):
    # Generate jwt token
    jwt_token = await user_context.generate_jwt_token().run(
        user=request.get('user'))

    response = ApiResponse().success()

    # Set jwt cookie
    await set_jwt_token_cookie(response, jwt_token)

    return response
