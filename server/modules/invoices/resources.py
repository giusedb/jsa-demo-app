from sqlalchemy import delete

from jsalchemy_api import DBResource, ResourceManager
from jsalchemy_api.resources.base import verb
from jsalchemy_web_context import db
from .models import Provider


class ProviderResouce(DBResource):

    def __init__(self, resource_manager: ResourceManager):
        super().__init__(
            name='Provider',
            model=Provider,
            resource_manager=resource_manager,
        )

    @verb(detached_instance=True)
    async def delete_all(self, a, b):
        """Delete all providers from the DataBase"""
        # await db.execute(delete(Provider))
        return f'suca {a=} {b=}'

    @verb
    async def on_instance(self, instance, num: int):
        instance.total_amount += num
        return f'Cippa {num} volte'