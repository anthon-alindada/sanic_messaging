# -*- coding: utf-8
import graphene
from graphene.types.resolver import attr_resolver


class UserType(graphene.ObjectType):
    id = graphene.Int()
    email = graphene.String()
    last_name = graphene.String()
    first_name = graphene.String()
    date_joined = graphene.Int()

    class Meta:
        default_resolver = attr_resolver

    def resolve_date_joined(self, info):
        return self.date_joined.strftime('%s')
