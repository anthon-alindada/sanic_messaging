# -*- coding: utf-8
# Core
from . import app
import string
import random
from datetime import datetime, timedelta


async def generate_token(
    size=64,
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits
):
    return ''.join(random.choice(chars) for _ in range(size))


async def is_ajax(request):
    is_ajax = False
    x_request_width = request.headers.get('x-requested-with', '')

    if str.lower(x_request_width) == 'xmlhttprequest':
        is_ajax = True

    return is_ajax


def set_cookie(
    response,
    name,
    value,
    httponly=False,
    max_age=None,
    secure=None,
    path='/',
):
    """
    Set cookie
    """

    # Set jwt cookie
    response.cookies[name] = value
    response.cookies[name]['httponly'] = httponly
    response.cookies[name]['max-age'] = max_age
    response.cookies[name]['path'] = path

    # Set security if none set default
    if secure is not None:
        response.cookies[name]['secure'] = secure
    else:
        response.cookies['jwt_token']['secure'] = app.config.get(
            'SECURE_COOKIE')


async def set_jwt_token_cookie(response, jwt_token):
    """
    Set jwt token and expiration in cookie helper
    """

    # Set jwt cookie
    response.cookies['jwt_token'] = jwt_token
    response.cookies['jwt_token']['httponly'] = True
    response.cookies['jwt_token']['max-age'] = 14400
    response.cookies['jwt_token']['secure'] = app.config.get(
        'SECURE_COOKIE')

    # Set jwt expiration cookie
    response.cookies['jwt_expiration'] = (datetime.now() + timedelta(
        minutes=15)).strftime('%s')
    response.cookies['jwt_expiration']['secure'] = app.config.get(
        'SECURE_COOKIE')
