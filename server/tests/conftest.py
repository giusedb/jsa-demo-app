"""
Comprehensive pytest conftest for the JSAlchemy demo-app server.

Provides async fixtures for in-memory SQLite, FakeRedis, authentication,
resource manager, and a test user pre-registered and logged in.
"""

import sys
import os
from pathlib import Path

# Ensure the server directory is on sys.path so we can import modules
_server_root = str(Path(__file__).resolve().parent.parent)
if _server_root not in sys.path:
    sys.path.insert(0, _server_root)

# ── dev-dependency paths (editable installs) ──────────────────────────
_libs = Path(_server_root).parent / "libs"
for _lib in ("jsa-api", "jsa-authentication", "jsa-authorization", "jsa-context"):
    _src = _libs / _lib
    # hatch-built packages have a src/ layout
    _pkg = _src / "src"
    if _pkg.is_dir() and str(_pkg) not in sys.path:
        sys.path.insert(0, str(_pkg))
    # some libs are flat (jsa-authentication, jsa-authorization)
    if str(_src) not in sys.path:
        sys.path.insert(0, str(_src))


import pytest
import pytest_asyncio
import fakeredis.aioredis
from sqlalchemy import select, event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from jsalchemy_web_context import ContextManager, db
from jsalchemy_api import ResourceManager, DBResource, WebResource
from jsalchemy_authentication.manager import AuthenticationManager

# ── Import ALL model modules so their tables are registered on BaseModel.metadata ──
from modules.base import BaseModel
from modules.base.auth import User, Identity
from modules.todos.models import Todo
from modules.invoices.models import Provider, Invoice, Line
from modules.apitest.models import (
    Alone, Master, Detail, MountPoint, Folder, File, Tag,
)

# ── Import ALL resource modules to make resource classes available ──
from modules.todos.resources import TodoResource
from modules.invoices.resources import ProviderResouce, InvoiceResource, LineResource
from modules.apitest.resources import (
    AloneResource, MasterResource, DetailResource,
    MountPointResource, FolderResource, FileResource, TagResource,
)


# ══════════════════════════════════════════════════════════════════════════
#  Fixtures
# ══════════════════════════════════════════════════════════════════════════

@pytest_asyncio.fixture
async def db_engine():
    """Create an async in-memory SQLite engine with FK enforcement."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False})

    # Enable foreign key enforcement (off by default in SQLite)
    @event.listens_for(engine.sync_engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session(db_engine):
    """Create an async session maker bound to the in-memory engine."""
    return async_sessionmaker(bind=db_engine, expire_on_commit=False, autoflush=True)


@pytest_asyncio.fixture
async def create_tables(db_engine):
    """Create all tables defined on BaseModel.metadata."""
    async with db_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield
    # Disable FK enforcement before dropping (SQLite ordering constraint)
    async with db_engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: sync_conn.exec_driver_sql("PRAGMA foreign_keys=OFF"))
        await conn.run_sync(BaseModel.metadata.drop_all)


@pytest_asyncio.fixture
async def context(session, create_tables):
    """Build a ContextManager with FakeRedis and auto-commit enabled."""
    fake_redis = fakeredis.aioredis.FakeRedis()
    ctx_mgr = ContextManager(session, fake_redis, auto_commit=True)
    yield ctx_mgr
    await fake_redis.aclose()


@pytest_asyncio.fixture
async def auth(context):
    """Build an AuthenticationManager configured for the demo Identity model."""
    # Config uses: identity-model=modules.base.auth.Identity, identified-by=email
    return AuthenticationManager(
        Identity,
        context=context,
        salt="$2b$05$/vgmzVaeg8BwTmFvVQlQ1.",
        identified_by="email",
    )


@pytest_asyncio.fixture
async def rm(context, auth):
    """Build a ResourceManager and register all available resources."""
    manager = ResourceManager(auth_man=auth, context=context, name="test-app")

    # Register every resource class we imported
    resources = [
        TodoResource,
        ProviderResouce,
        InvoiceResource,
        LineResource,
        AloneResource,
        MasterResource,
        DetailResource,
        MountPointResource,
        FolderResource,
        FileResource,
        TagResource,
    ]
    for rcls in resources:
        instance = rcls(manager)
        # __init__ already calls manager.register(self) for DBResource
        # but let's be explicit for safety
        manager.register(instance)

    return manager


@pytest_asyncio.fixture
async def test_user(rm):
    """Register a test user and return a dict with token, user_id, and email."""
    user_data = {
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "secret123",
    }
    await rm.auth_man.register(user_data)
    result = await rm.login("testuser@example.com", "secret123")
    assert result is not None, "Login after registration must succeed"
    return {
        "token": result["token"],
        "user_id": result["user_id"],
        "email": "testuser@example.com",
        "password": "secret123",
    }