# -*- coding: utf-8
import graphene

# Decorators
from ..decorators import auth_required, csrf

# Types
from .types import UserType


class UserQuery(graphene.ObjectType):
    viewer = graphene.Field(UserType)

    @csrf
    @auth_required
    async def resolve_viewer(_, info):
        return info.context.get('user')
