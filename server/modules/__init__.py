import os
from typing import Iterable

from click import style

from jsalchemy_api import ResourceManager, WebResource, DBResource
from logging import getLogger
log = getLogger('JSAlchemy.init')


def depp_scan_modules(path=None):
    import pkgutil

    if not path:
        path = os.sep.join(__file__.split(os.sep)[:-1])
    l_base = len(__path__[0])-len(__package__)
    for mod in pkgutil.iter_modules([path]):
        if mod.ispkg:
            yield from depp_scan_modules(mod.module_finder.path + os.sep + mod.name)
            continue
        package_name = mod.module_finder.path[l_base:].replace(os.sep, '.')
        yield f'{package_name}.{mod.name}', [mod.name]

def get_all_models(BaseModelClass, excludes:Iterable[str]=()):
    """scans all `models` packages within the `modules` package and loads them"""
    for name, fromlist in depp_scan_modules():
        if fromlist == ['models']:
            log.info(f"importing {style('model', fg='cyan')} module from {style(name + '.' + fromlist[0], fg='yellow')}")
            mod = __import__(name, fromlist=fromlist)
            for attr_name, attr in mod.__dict__.items():
                if attr_name.startswith('_'):
                    continue
                if isinstance(attr, type) and issubclass(attr, BaseModelClass) and attr is not BaseModelClass:
                    log.info(f" -> {style(attr_name, fg='green')} ✅")
                    yield attr_name, attr


def init_all_resources(rm: ResourceManager, excludes:Iterable[str]=()):
    """scan all `resources` packages within the `modules` package and loads them."""
    for name, fromlist in depp_scan_modules():
        if fromlist == ['resources']:
            log.info(f"importing {style('resource', fg='cyan')} module from {style(name + '.' + fromlist[0], fg='yellow')} ")
            mod = __import__(name, fromlist=fromlist)
            for attr_name, attr in mod.__dict__.items():
                if attr_name.startswith('_'):
                    continue
                if isinstance(attr, type) and issubclass(attr, WebResource) and attr not in {WebResource, DBResource}:
                    log.info(f" -> registering {style(attr_name, fg='green')} ✅")
                    instance = attr(rm)
                    rm.register(instance)
