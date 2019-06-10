# -*- coding: utf-8
import os
from sanic import Sanic
from gino.ext.sanic import Gino
from simple_bcrypt import Bcrypt
from sanic_jinja2 import SanicJinja2
from sanic_graphql import GraphQLView

# Configs
from config import config

# Domain Applications
from app.domain.user import init_user_app
from app.domain.messaging import init_messaging_app

# Html application
from app.http import init_http_app


# Orm database
db = Gino()

# Bcrypt
bcrypt = Bcrypt()

# Jinja template library
jinja = SanicJinja2()


def create_app(config_name=None):
    """
    Create sanic application
    """
    if config_name is None:
        config_name = os.environ.get('SANIC_APP_CONFIG', 'development')

    # Get configuration object
    config_object = config[config_name]

    # Sanic app
    app = Sanic(__name__)
    app.config.from_object(config_object)

    # Setup Gino orm
    db.init_app(app)

    # Setup Bcrypt
    bcrypt.init_app(app)

    # Setup jinja
    jinja.init_app(app, pkg_path='http/templates')

    """
    Initialize domain application
    """
    init_user_app(app, db, bcrypt)
    init_messaging_app(app, db)

    """
    Initialize http applications
    """
    init_http_app(app, jinja)

    """
    Initialize blueprints
    """
    from .http.core.views import core_views
    from .http.signup.views import signup_views
    from .http.auth.views import auth_views

    """
    Initialize blueprints
    """
    app.blueprint(core_views, url_prefix='/')
    app.blueprint(auth_views, url_prefix='/')
    app.blueprint(signup_views, url_prefix='/')

    # Static
    STATIC_FOLDER = os.path.join(os.path.dirname(__file__), 'static/dist')
    app.static('/static', STATIC_FOLDER)

    """
    Initialize graphql
    """
    @app.listener('before_server_start')
    async def init_graphql(app, loop):
        # Disable graphql route if testing
        if config_name != 'test':
            from .http.graphql import schema
            from graphql.execution.executors.asyncio import AsyncioExecutor
            app.add_route(GraphQLView.as_view(
                schema=schema,
                executor=AsyncioExecutor(loop=loop),
                graphiql=True,
            ), '/graphql')

    return app
