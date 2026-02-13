from sqlalchemy import delete, select
from sqlalchemy.orm import DeclarativeBase

from jsalchemy_api import DBResource
from jsalchemy_api.resources.base import verb
from jsalchemy_web_context import db
from .models import Master, Alone, Detail

import logging
log = logging.getLogger('resource.test')


class Deletable:

    model: DeclarativeBase

    @verb(detached_instance=True)
    async def delete_all(self):
        await db.execute(delete(self.model).where(self.model.id > 0))

    @verb(detached_instance=True)
    async def delete_all_one_at_time(self):
        all_items = (await db.execute(select(self.model))).scalars()
        db.delete(all_items)


class AloneResource(DBResource):

    def __init__(self, resource_manager):
        super().__init__(resource_manager, name='Alone', model=Alone)

    @verb(detached_instance=True)
    async def delete_all(self):
        await db.execute(delete(self.model).where(self.model.id > 0))

    @verb(detached_instance=True)
    async def delete_all_one_at_time(self):
        for item in (await db.execute(select(self.model))).scalars().all():
            db.delete(item)

    @verb(detached_instance=True)
    async def get_all(self):
        items = (await db.execute(select(self.model))).scalars().all()
        return {
            'items': items,
            'count': len(items)
        }



class MasterResource(DBResource):

    def __init__(self, rm):
        super().__init__(rm, 'Master', model=Master)

    def non_verb(self, a, b):
        """Non verb method"""
        log.info('Non verb called with %s %s.', a, b)


    @verb
    def instance_get(self, instance):
        """Method without attribute"""
        log.info('Calling method with instance')
        return instance

    @verb
    def instance_echo(self, instance, ping):
        return ping

    @verb(detached_instance=True)
    def class_echo(self, a='echo'):
        return a

class DetailResource(Deletable, DBResource):
    def __init__(self, rm):
        super().__init__(rm, 'Detail', model=Detail)
