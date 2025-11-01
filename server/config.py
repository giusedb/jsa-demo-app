import os
from functools import lru_cache

import yaml

from jsalchemy_api.utils import dict_merge

default_config = dict(
    web=dict(
        port=7999,
        host='0.0.0.0',
        use_cookies=False,
        token_key='__token__',
        realtime=False,
        reload=False,
        root_endpoint='/JSAlchemy',
        session=dict(
            connection="redis://127.0.0.1:6379/1"
        ),
        auth=dict(
            salt='replace me'
        )
    ),
    db=dict(
        connection=dict(
            string='sqlite+aiosqlite:///:memory:',
            pool=50
        )
    ),
)

@lru_cache(1)
def get_config():
    current_dir = os.path.dirname(__file__)
    config_file = os.path.join(current_dir, 'config.yaml')
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return dict_merge(yaml.load(f, Loader=yaml.FullLoader), default_config)
    return default_config


def setup_log():
    import os
    from logging import config as log_config
    import yaml

    conf_file = os.sep.join(__file__.split(os.sep)[:-1] + ['logging.yaml'])
    if os.path.exists(conf_file):
        with open(conf_file) as f:
            conf_dict = yaml.load(f, Loader=yaml.SafeLoader)
        log_config.dictConfig(conf_dict)

