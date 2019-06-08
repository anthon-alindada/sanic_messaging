# -*- coding: utf-8
# Core
import os
from jinja2 import Environment, FileSystemLoader

# Dependency injector
from dependency_injector import containers
from dependency_injector import providers


app = None
db = None
bcrypt = None
jinja = Environment(loader=FileSystemLoader(
    os.path.join(os.path.dirname(__file__), 'templates')))


# User context
user_context = containers.DynamicContainer()


def init_user_app(
    app_instance,
    db_instance,
    bcrypt_instance,
):
    global app
    global db
    global bcrypt

    app = app_instance
    db = db_instance
    bcrypt = bcrypt_instance

    # Stores
    from .stores.user_store import UserStore

    # Query sets
    from .query_sets.user_query import UserQuery

    # Forms
    from .forms.signup_form import SignupForm

    # Libs
    from .libs.signup import Signup
    from .libs.login import Login
    from .libs.generate_jwt_token import GenerateJwtToken

    # Authentication
    from .authentication import PasswordAuthentication
    from .authentication import JwtAuthentication

    # Set user context
    # Set dependency injector providers
    # Stores
    user_context.user_store = providers.Singleton(UserStore)

    # Query sets
    user_context.user_query = providers.Factory(UserQuery)

    # Forms
    user_context.signup_form = providers.Object(SignupForm)

    # Authentication
    user_context.password_authentication = providers.Singleton(
        PasswordAuthentication, user_query=user_context.user_query)
    user_context.jwt_authentication = providers.Singleton(
        JwtAuthentication, user_query=user_context.user_query)

    # Libs
    user_context.signup = providers.Factory(
        Signup,
        user_query=user_context.user_query,
        signup_form=user_context.signup_form,
        user_store=user_context.user_store)
    user_context.login = providers.Factory(
        Login,
        user_query=user_context.user_query,
        password_authentication=user_context.password_authentication)
    user_context.generate_jwt_token = providers.Factory(GenerateJwtToken)
