# -*- coding: utf-8
from sanic import Blueprint
from .. import app, jinja

# Security
from secure import SecureHeaders

# Helper
from ..helpers import generate_token

# Decorator
from ..decorators import auth_required


core_views = Blueprint('core', __name__)

secure_headers = SecureHeaders()


@core_views.middleware('response')
async def add_csrf_token_cookie(request, response):
    """
    Set csrf token in cookie
    """
    token = await generate_token()

    # Set secure httponly csrf token
    response.cookies['t'] = token
    response.cookies['t']['httponly'] = True
    response.cookies['t']['secure'] = app.config.get('SECURE_COOKIE')

    # Set public csrf token for javascript
    response.cookies['csrf_token'] = token
    response.cookies['csrf_token']['secure'] = app.config.get('SECURE_COOKIE')

    # Secure all header response
    secure_headers.sanic(response)


@core_views.route('/', methods=['GET'])
@jinja.template('core/index.html')
@auth_required()
async def index(request):
    return {'user': request.get('user')}
