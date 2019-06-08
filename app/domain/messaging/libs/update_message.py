# -*- coding: utf-8
# Exception
from ..exceptions import InvalidInput


class UpdateMessage:
    """
    Update message library
    """

    def __init__(
        self,
        update_message_form,
        message_store,
    ):
        # Library
        self.update_message_form = update_message_form
        self.message_store = message_store

        # Errors
        self._errors = {}

    async def run(self, message_instance, content, author_id):
        # Validate update message form
        update_message_form = self.update_message_form(data={
            'content': content,
        })

        await update_message_form.set_message_instance(message_instance)
        await update_message_form.set_author_id(author_id)

        if update_message_form.validate() is False:
            self._errors = update_message_form.errors
            raise InvalidInput

        # Update message
        message = await self.message_store.set_content(
            message=message_instance, content=content)

        return message

    async def get_errors(self):
        return self._errors
