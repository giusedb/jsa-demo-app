import click

from .base import main

@main.group()
def web():
    """Web section"""

@web.command()
@click.option('-D', '--debug', is_flag=True, default=False)
@click.option('-p', '--port', default=8000, type=int)
@click.option('-s', '--host', default='0.0.0.0')
def fastapi(host, port, debug):
    """Run web dev server"""
    import uvicorn
    uvicorn.run('web_app.fastapp:app', host=host, port=port, reload=debug)@web.command()

@web.command()
@click.option('-D', '--debug', is_flag=True, default=False)
@click.option('-p', '--port', default=8000, type=int)
@click.option('-s', '--host', default='0.0.0.0')
def blacksheep(host, port, debug):
    """Run web dev server"""
    import uvicorn
    uvicorn.run('web.blacksheep:app', host=host, port=port, reload=debug)