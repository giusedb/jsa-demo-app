import os
import sys

import click
from orjson import orjson
from sqlalchemy.ext.asyncio import async_sessionmaker

from jsalchemy_api.application import setup_application
from modules.base import get_engine, BaseModel
from .utils import beautify
from .base import main


@main.group()
def db():
    """Database operations"""

@db.command(name='import')
@click.argument('path', type=click.Path(exists=True))
def inport(path: str):
    """import a fixture."""
    from data import models
    if not os.path.exists(path):
        click.echo(f"Sorry, {click.style('File not found', fg='red')}")
    import orjson
    with open(path, 'r') as f:
        content = orjson.loads(f.read())
    filename = os.sep.split(path)


@db.command()
@click.argument('comment', type=str)
def migrate(comment):
    """Generate an alembic migration script."""
    os.system(f'alembic revision -m "{comment}" --autogenerate')

@db.command()
@click.option('-r', '--revision', type=str, default='head', help='Revision to migrate to.')
def upgrade(revision='head'):
    """Upgrade the database structure."""
    os.system(f'alembic upgrade {revision}')


@db.command()
@click.option('-r', '--revision', type=str, default='-1', help='Revision to migrate to.')
def downgrade(revision):
    """Downgrade the database structure to the previous revision."""
    os.system(f'alembic downgrade {revision}')

@db.command()
def list():
    """Shows all the available revisions."""
    os.system(f'alembic history')


@db.command()
@click.option('-r', '--revision', type=str, default='head', help='Revision to show.')
def show(revision='head'):
    """Show the migration script for the specified revision."""
    script_dir = 'scripts/versions'
    files = [f for f in os.listdir(script_dir) if os.path.isfile(os.path.join(script_dir, f))]
    if revision == 'head':
        files.sort(key=lambda x: os.path.getmtime(os.path.join(script_dir, x)))
        os.system(f"bat {script_dir}/{files[0]}")
    else:
        files = tuple(filter(lambda x: x.startswith(revision), files))
        os.system(f"bat {script_dir}/{files[0]}")

@db.command()
@click.option('-p', '--password', default=None, help='Creates an admin user with password')
def init(password):
    """Initialize the database."""
    from config import get_config
    import asyncio
    from modules import get_all_models
    from click import style

    conf = get_config()
    beautify(conf)

    for name, model in get_all_models(BaseModel):
        print(f"Model {style(name, fg='green')} loaded")

    print(" -> Connecting to DB ...")
    engine, _ = get_engine(conf['db'])
    print(" -> Creating tables to DB ...")
    res_man = setup_application(get_config())

    async def init_db():
        async with res_man.context.session_maker().bind.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)
            await conn.run_sync(BaseModel.metadata.create_all)

    async def create_user():
        from modules.base.auth import User, Identity
        from jsalchemy_web_context import db
        async with res_man.context():
            print(" -> Creating the admin user to DB ...")
            user = User(first_name='Super', last_name='Admin')
            db.add(user)
            db.flush()
            identity = Identity(email='admin@admin.com', password=password, user=user)
            db.add(identity)
            await db.commit()

    async def make():
        await init_db()
        if password:
            await create_user()
    asyncio.run(make())
    print(" <- Done. 👍")

@db.command()
def fixture(name):
    """Import a fixture."""
    filepath = os.path.join(os.path.dirname(__file__), 'fixtures', f"{name}.json")
    if not os.path.exists(filepath):
        print(f"Sorry, {click.style('File not found', fg='red')}")
        sys.exit(1)
    with open(filepath, 'r') as f:
        content = orjson.loads(f.read())
