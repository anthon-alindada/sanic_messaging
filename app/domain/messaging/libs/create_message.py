# -*- coding: utf-8
# Exception
from ..exceptions import InvalidInput


class CreateMessage:
    """
    Crate message library
    """

    def __init__(
        self,
        create_message_form,
        message_store,
    ):
        # Library
        self.create_message_form = create_message_form
        self.message_store = message_store

        # Errors
        self._errors = {}

    async def run(self, content, author_id, channel_id):
        # Validate create message form
        create_message_form = self.create_message_form(data={
            'content': content,
        })

        if create_message_form.validate() is False:
            self._errors = create_message_form.errors
            raise InvalidInput

        # Create new message
        message = await self.message_store.create(
            author_id=author_id,
            channel_id=channel_id,
            content=content)

        return message

    async def get_errors(self):
        return self._errors
