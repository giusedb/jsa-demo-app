from sqlalchemy import delete, select

from jsalchemy_api import DBResource, ResourceManager
from jsalchemy_api.resources.base import verb
from jsalchemy_web_context import db
from modules.todos.models import Todo


class TodoResource(DBResource):
    def __init__(self, resource_manager: ResourceManager):
        super().__init__(
            model=Todo,
            name='Todo',
            resource_manager=resource_manager,
            rpp=100,
        )

    @verb(detached_instance=True)
    async def delete_all(self):
        await db.execute(delete(self.model).where(self.model.id > 0))