import click

from modules import get_all_models


@click.group()
@click.pass_context
def main(ctx):
    """JSAlchemy scaffolding app"""
    from config import setup_log, get_config
    setup_log()
    ctx.ensure_object(dict)
    ctx.obj['config'] = get_config()


n = 1
imported = set()

@main.command()
def shell():
    """Enter the shell with preloaded environment."""
    from IPython.terminal.ipapp import TerminalIPythonApp
    from sqlalchemy import select, text, insert, update, delete
    from jsalchemy_web_context import session as web_session
    from jsalchemy_api.application import base_environment
    from config import get_config
    from modules.base import get_sync_engine, BaseModel
    from modules.base.auth import User
    import datetime
    import time

    def module_update(mod, ctx):
        attrs = {name: attr for name, attr in mod.__dict__.items() if isinstance(name, str) and not name.startswith('_')}
        ctx.update(**attrs)

    class Session:

        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    ctx = dict(get_all_models(BaseModel))

    ctx.update(select=select, text=text, update=update, delete=delete, insert=insert)
    ctx['User'] = User
    module_update(time, ctx)
    module_update(datetime, ctx)

    ipython_app = TerminalIPythonApp.instance(user_ns=ctx, display_banner=False)
    ipython_app.initialize(argv=[])
    ipython_app.shell.show_banner('Welcome to my App 😎')

    context = base_environment(get_config(), sync=True)
    with context():
        from jsalchemy_web_context.sync import db, session
        web_session.update(Session(user=session.get(User, 1)))
        ctx['db'] = db
        ctx['session'] = web_session
        web_session.user = session.get(User, 1)
        ipython_app.start()
