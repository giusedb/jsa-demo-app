from jsalchemy_api import DBResource, ResourceManager
from .models import Car, Manifacturer


class CarResource(DBResource):

    def __init__(self, resource_manager: ResourceManager):
        DBResource.__init__(self, resource_manager=resource_manager,
                            model=Car, rpp=200, name='Car')


class ManifacturerResource(DBResource):

    def __init__(self, resource_manager: ResourceManager):
        DBResource.__init__(self, resource_manager=resource_manager,
                            model=Manifacturer, rpp=200, name='Manifacturer')
