from datetime import date
from typing import List

from sqlalchemy import ForeignKey, Integer, JSON, Float, Date
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column, Table, Column

from modules.base import BaseModel

class NamedMixin:

    name: Mapped[str] = mapped_column('name', nullable=False, index=True)

    def __repr__(self):
        return f'<{self.__class__.__name__}({self.name!r})>'

class Alone(NamedMixin, BaseModel):

    __tablename__ = 'alone'
    score: Mapped[float] = mapped_column(Float, nullable=True)
    date: Mapped[date] = mapped_column(Date, nullable=True)

class Master(NamedMixin, BaseModel):
    __tablename__ = 'master'

    score: Mapped[int]
    description: Mapped[str] = mapped_column(nullable=True)


class Detail(NamedMixin, BaseModel):

    __tablename__ = 'detail'
    score: Mapped[int]
    description: Mapped[str] = mapped_column(nullable=True)
    master_id: Mapped[int] = mapped_column(ForeignKey(Master.id))

    master: Mapped[Master] = relationship(Master, backref='details')

class Node(NamedMixin, BaseModel):
    __tablename__ = 'node'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    parent_id: Mapped[int] = mapped_column(ForeignKey('node.id'))

    parent: Mapped['Node'] = relationship('Node', remote_side=[id])
    children: Mapped[List['Node']] = relationship('Node', remote_side=[parent_id], uselist=True)

class One(NamedMixin, BaseModel):
    __tablename__ = 'one'

class Two(NamedMixin, BaseModel):
    __tablename__ = 'two'

m2m_1to2 = Table(
   'one_to_two',
    BaseModel.metadata,
    Column('one_id', Integer(), ForeignKey('one.id')),
    Column('two_id', Integer(), ForeignKey('two.id')),
)

One.twos = relationship(Two, secondary=m2m_1to2)
Two.onex = relationship(One, secondary=m2m_1to2)


class Folder(NamedMixin, BaseModel):
    __tablename__ = 'folder'

    mounts_id: Mapped[int] = mapped_column(ForeignKey('mount_point.id'), nullable=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('folder.id'), nullable=True)

    children: Mapped[List['Folder']] = relationship('Folder', remote_side=[parent_id], uselist=True)
    mounts: Mapped['MountPoint'] = relationship('MountPoint', primaryjoin='Folder.mounts_id == MountPoint.id')

Folder.parent: Mapped['Folder'] = relationship('Folder', remote_side=[Folder.id])



class MountPoint(NamedMixin, BaseModel):
    __tablename__ = 'mount_point'

    root_id: Mapped[int] = mapped_column(ForeignKey('folder.id'), nullable=True)
    options: Mapped[dict] = mapped_column(JSON, default={})

    root: Mapped['Folder'] = relationship(Folder, primaryjoin=root_id == Folder.id)


class File(NamedMixin, BaseModel):
    __tablename__ = 'file'

    folder_id: Mapped[int] = mapped_column(ForeignKey('folder.id'), nullable=False)
    folder: Mapped[Folder] = relationship('Folder', primaryjoin=folder_id == Folder.id, backref='files')

class Tag(NamedMixin, BaseModel):
    __tablename__ = 'tag'

    color: Mapped[str]

tags_file = Table(
    'tag_file',
    BaseModel.metadata,
    Column('tag_id', Integer(), ForeignKey('tag.id')),
    Column('file_id', Integer(), ForeignKey('file.id')),
)

tags_folder = Table(
    'tag_folder',
    BaseModel.metadata,
    Column('tag_id', Integer(), ForeignKey('tag.id')),
    Column('folder_id', Integer(), ForeignKey('folder.id')),
)

Tag.files = relationship(File, secondary=tags_file, backref='tags')
Tag.folders = relationship(Folder, secondary=tags_folder, backref='tags')