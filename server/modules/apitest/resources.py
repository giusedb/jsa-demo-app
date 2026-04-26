import os
from typing import List, Dict

import yaml
from sqlalchemy import delete, select, func
from sqlalchemy.orm import DeclarativeBase
from yaml import SafeLoader

from jsalchemy_api import DBResource
from jsalchemy_api.resources.base import verb
from jsalchemy_web_context import db
from .models import Master, Alone, Detail, MountPoint, Folder, File, Tag

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



class MasterResource(Deletable, DBResource):

    def __init__(self, rm):
        Deletable.__init__(self)
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


class MountPointResource(Deletable, DBResource):
    def __init__(self, rm):
        super().__init__(rm, 'MountPoint', model=MountPoint, format_string='${this.name}')

    @verb(detached_instance=True)
    async def run_fixture(self) -> dict:
        """Import the filesystem fixture."""

        def import_folders(folder: Folder, children: List[Dict | str]) -> None:
            for child in children:
                if isinstance(child, str):
                    db.add(File(name=child, folder=folder))
                elif isinstance(child, dict):
                    for name, inner in child.items():
                        if name == 'mount':
                            folder.mounts = mounts['home']
                            continue
                        child_folder = Folder(name=name, parent=folder)
                        db.add(child_folder)
                        import_folders(child_folder, inner)


        with open(os.sep.join(os.path.dirname(__file__).split(os.sep)[:-2] + ['fixtures', 'file-system.yaml'])) as f:
            fixture = yaml.load(f, SafeLoader)
        max_mount_point_id = (await db.execute(select(func.max(MountPoint.id)))).scalar()
        max_folder_id = (await db.execute(select(func.max(Folder.id)))).scalar()
        max_file_id = (await db.execute(select(func.max(File.id)))).scalar()

        mounts = {}
        for name, op in fixture.items():
            mp = MountPoint(name=name, options=op.get('options', {}))
            mounts[name] = mp
            root = op.get('root')
            if root:
                root_folder = Folder(name='root')
                import_folders(root_folder, root)
                mp.root = root_folder
            db.add(mp)
        await db.execute(delete(File).where(File.id <= max_file_id))
        await db.execute(delete(Folder).where(Folder.id <= max_folder_id))
        await db.execute(delete(MountPoint).where(MountPoint.id <= max_mount_point_id))

        return fixture

class FolderResource(Deletable, DBResource):
    def __init__(self, rm):
        super().__init__(rm, 'Folder', model=Folder, format_string='${this.name}')

class FileResource(Deletable, DBResource):
    def __init__(self, rm):
        super().__init__(rm, 'File', model=File, format_string='${this.name}')

class TagResource(Deletable, DBResource):
    def __init__(self, rm):
        super().__init__(rm, 'Tag', model=Tag, format_string='${this.name}')
