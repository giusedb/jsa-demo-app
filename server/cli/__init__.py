def main_cli():
    from .db import db
    from .web import web
    from .base import main

    return main()
