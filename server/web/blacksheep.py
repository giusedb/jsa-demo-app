import sys
import traceback
import uuid
from datetime import datetime

import aiofile
import orjson
from blacksheep import Application, post, Response, Content, HTTPException, get, FromFiles
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info

from config import get_config, setup_log
from jsalchemy_api.application import setup_application
from jsalchemy_api.exceptions import JSAlchemyException
from modules import init_all_resources

import logging

logger = logging.getLogger('JSAlchemy.web')

app = Application()
docs = OpenAPIHandler(info=Info(
    title='JSAlchemy test application', version='0.1.0', description='JSAlchemy test application'))
docs.bind_app(app)
setup_log()

config = get_config()
rm = setup_application(config)

init_all_resources(rm)

# locally used configuration
root_endpoint = config['web']['root_endpoint']
token_key = config['web']['token_key']

def json_response(d: dict, status=200):
    return Response(
        status, content=Content(
            content_type=b'application/json',
            data=orjson.dumps(d),
        ))

@get(f"{root_endpoint}/config")
def setup() -> dict:
    forbidden = 'port', 'host', 'session', 'auth'
    return json_response({ key: value for key, value in config['web'].items() if key not in forbidden })

@post(f'{root_endpoint}/auth/login')
async def login(body: dict) -> str:
    """Login and return the session token."""
    username, password = body.get('username'), body.get('password')
    ret = await rm.login(username, password)
    if not ret:  # s
        return json_response({'error': 'Invalid username or password.'}, 403)
    return ret

@post(f'{root_endpoint}/auth/logout')
async def logout(body: dict) -> str:
    token = body.get(token_key)
    ret = await rm.logout(token)
    return ret

@post(f'{root_endpoint}/auth/register')
async def register(body: dict) -> str:
    """Register a new user"""
    try:
        if await rm.auth_man.user_exists(body['username']):
            return json_response({'error': 'Username already exists', 'ts': datetime.now()}, 401)
        return await rm.auth_man.register(body)
    except Exception as e:
        traceback.print_tb(sys.exc_info()[2])
        raise HTTPException(500, 'suca')

@post(root_endpoint + r"/{action}")
async def jsalchemy(action: str, body: dict) -> Response:
    if '.' not in action:
        return json_response(
            {'error': "Invalid URL it must be in the for /jsalchemy/{model}.{verb}",
             'ts': datetime.utcnow()}, 400)
    resource, verb = action.split('.', 1)
    token = body.pop(token_key, None)
    if not token:
        return json_response({'error': "Connection unidentified. Please login", 'ts': datetime.utcnow()}, 403)
    try:
        return json_response(await rm.action(token, resource, verb, **body))
    except JSAlchemyException as e:
        return json_response({ 'error': e.message, 'ts': datetime.now()}, e.status_code)
    except Exception as e:
        tb = traceback.format_tb(sys.exc_info()[2])
        logger.error('Error while executing action %s.%s', resource, verb, exc_info=e)
        return json_response({'error': str(e), 'ts': datetime.now(), 'traceback': tb}, 500)

@get('/{path:path}')
async def catch_all(path: str) -> Response:
    logger.info(f'Got a GET form "{path}"')
    return json_response({'error': 'Not found', 'ts': datetime.now()}, 404)

@post('/{path:path}')
async def catch_all(path: str, body: dict) -> Response:
    logger.info(f'Got a POST form "{path}" with body {body}')
    return json_response({'error': 'Not found', 'ts': datetime.now()}, 404)

@post('/files/upload/{folder_id}/{token}')
async def upload_files(folder_id: int, token: str, files: FromFiles) -> Response:
    ret = []
    for file in files.value:
        filename = str(uuid.uuid4())
        real_path = f"uploads/{filename}.bin"
        async with aiofile.async_open(real_path, 'wb') as f:
            await f.write(file.data)

        ret.append(await rm.action(token, 'file', 'post', **{
            'folder_id': folder_id, 'name': file.file_name.decode('utf-8'), 'size': len(file.data),
            'mime_type': file.content_type.decode('ascii'), 'fs_path': real_path, 'md5': '{}'}))

    return json_response({'new': {'File': [x['new']['File'][0] for x in ret]}}, 200)
