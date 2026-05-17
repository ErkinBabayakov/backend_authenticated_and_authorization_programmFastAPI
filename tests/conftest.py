# ruff: noqa: E402
import pytest

from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
from src.api.dependencies import get_db
from src.main import app
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.models import *  # noqa
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


# Перезаписывам зависимость с session_factory=async_session_maker на async_session_maker_null_pool (
app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in get_db_null_pool():
        yield db


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/register",
        json={
            "email": "kot@pes.com",
            "first_name": "kot",
            "last_name": "pes",
            "password": "1234",
            "retry_password": "1234",
            "is_admin": True,
        },
    )


@pytest.fixture(scope="session", autouse=True)
async def authenticated_ac(ac, register_user):
    await ac.post("/auth/login", json={"email": "kot@pes.com", "password": "1234"})
    assert ac.cookies["access_token"]
    yield ac
