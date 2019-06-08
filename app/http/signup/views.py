# -*- coding: utf-8
from sanic import Blueprint
from .. import jinja
from ..api_response import ApiResponse

# Decorator
from ..decorators import csrf, guest_only

# Context
from app.domain.user import user_context

# Exception
from app.domain.user.exceptions import InvalidInput

# Helpers
from ..helpers import set_jwt_token_cookie


signup_views = Blueprint('signup', __name__)


@signup_views.route('/signup', methods=['GET'])
@jinja.template('signup/signup.html')
@guest_only()
async def signup(request):
    return {}


@signup_views.route('/api/signup', methods=['POST'])
@csrf()
@guest_only()
async def api_signup(request):
    if request.method == 'POST':
        # Signup library
        signup_lib = user_context.signup()

        try:
            user = await signup_lib.run(
                first_name=request.json.get('first_name', ''),
                last_name=request.json.get('last_name', ''),
                email=request.json.get('email', ''),
                password=request.json.get('password', ''),
                confirm_password=request.json.get('confirm_password', ''))

            # Generate jwt token
            jwt_token = await user_context.generate_jwt_token().run(user=user)

            # Return jwt token
            response = ApiResponse().success(data=jwt_token)

            # Set jwt cookie
            await set_jwt_token_cookie(response, jwt_token)

            return response
        except InvalidInput:
            return ApiResponse().unprocessable_entity(
                data=await signup_lib.get_errors())
