import click

from config import get_config
from .base import main

@main.group()
def web():
    """Web section"""

def parse_web_defaults(cli: dict):
    config = get_config()
    web_config = config.get('web', {})
    web_default = {
        'host': '0.0.0.0',
        'port': 8000,
        'debug': False,
    }
    parsed = {key: web_config.get(key) or cli.get(key) or web_default[key] for key in cli}
    return parsed


@web.command()
@click.option("-D", "--debug", is_flag=True, default=False)
@click.option("-p", "--port", default=None, type=int)
@click.option("-s", "--host", default="0.0.0.0")
def fastapi(host, port, debug):
    """Run web dev server"""
    import uvicorn
    cli = dict(host=host, port=port, debug=debug)
    uvicorn.run('web_app.fastapp:app', **parse_web_defaults(cli))

@web.command()
@click.option('-D', '--debug', is_flag=True, default=False)
@click.option('-p', '--port', default=8000, type=int)
@click.option('-s', '--host', default='0.0.0.0')
def blacksheep(host, port, debug):
    """Run web dev server"""
    import uvicorn
    cli = parse_web_defaults(dict(host=host, port=port, debug=debug))
    cli['reload'] = cli.pop('debug')
    uvicorn.run('web.blacksheep:app', **cli)

@web.command()
@click.option('-h', '--host', default=None)
@click.option('-p', '--port', default=None)
@click.option('-c', '--redis-channel', default=None)
def realtime(host, port, redis_channel):
    """Run realtime server"""
    from jsalchemy_api.realtime import WSServer

    config = get_config().get('web')
    rt_config = config.get('realtime')
    if rt_config is False:
        raise click.ClickException("Realtime server is explitely disabled py configuration")

    print(f"🚀 Starting realtime server on {rt_config['host']}:{rt_config['port']}")

    server = WSServer(
        host=rt_config['host'],
        port=rt_config['port'],
        redis_channel=rt_config['redis_channel'],
        redis_url=config.get('session', {}).get('connection'),
    )

    server.start()
