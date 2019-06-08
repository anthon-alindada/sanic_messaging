# -*- coding: utf-8


class BaseQuery():
    """
    Base query set
    """

    _model = None
    _query = None

    @classmethod
    def new(cls):
        return cls()

    async def find(self):
        """
        Get first entity
        return is None or Model instance
        """
        return await self._query.gino.first()

    async def filter(self):
        """
        Get all entities
        return is array of model instance
        """
        return await self._query.gino.all()
