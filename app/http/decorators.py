# -*- coding: utf-8
# Core
from functools import wraps
from sanic.response import redirect
from .api_response import ApiResponse

# Helpers
from .helpers import is_ajax

# Contexts
from app.domain.user import user_context


def csrf():
    """
    Validate csrf token header and cookie if matched
    """

    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # If request method is POST
            # Validate csrf
            if request.method == 'POST':
                csrf_token_cookie = request.cookies.get('t', None)
                csrf_token_input = request.headers.get(
                    'x-csrf-token', None) or request.form.get(
                        'csrf_token', None)

                # If csrf header or cookies are either None
                if csrf_token_cookie is None or csrf_token_input is None:
                    if await is_ajax(request):
                        return ApiResponse().forbidden()
                    else:
                        return redirect(request.url)

                # If csrf tokens are mismatched
                if csrf_token_cookie != csrf_token_input:
                    if await is_ajax(request):
                        return ApiResponse().forbidden()
                    else:
                        return redirect(request.url)

            # If csrf is valid
            response = await f(request, *args, **kwargs)
            return response

        return decorated_function
    return decorator


def auth_required():
    """
    Validate authentications
    Jwt authentication
    """

    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            jwt_token = request.cookies.get('jwt_token', '')

            # Validate jwt token
            user = await user_context.jwt_authentication().authenticate(
                token=jwt_token)

            # If user does not exist
            # Return unauthorized
            if user is None:
                if await is_ajax(request):
                    response = ApiResponse().unauthorized()
                else:
                    response = redirect('/login')

                # Auto logout
                # Delete jwt_token cookie
                del response.cookies['jwt_token']
                return response

            # Set user
            request['user'] = user
            response = await f(request, *args, **kwargs)
            return response

        return decorated_function
    return decorator


def guest_only():
    """
    Validate guest only
    """

    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            jwt_token = request.cookies.get('jwt_token', None)

            if jwt_token is not None:
                if await is_ajax(request):
                    response = ApiResponse().unauthorized()
                else:
                    response = redirect('/')

                return response

            # Return
            response = await f(request, *args, **kwargs)
            return response

        return decorated_function
    return decorator
