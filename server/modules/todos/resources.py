from jsalchemy_api import DBResource, ResourceManager
from modules.todos.models import Todo


class TodoResource(DBResource):
    def __init__(self, resource_manager: ResourceManager):
        super().__init__(
            model=Todo,
            name='Todo',
            resource_manager=resource_manager
        )
