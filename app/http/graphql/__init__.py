# -*- coding: utf-8
import graphene

# Queries
from .user.queries import UserQuery


class RootQuery(UserQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=RootQuery)
