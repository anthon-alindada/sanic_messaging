# -*- coding: utf-8


class BaseStore():
    """
    Base store
    """

    _update_query = None

    async def save(self):
        return await self._update_query.apply()
