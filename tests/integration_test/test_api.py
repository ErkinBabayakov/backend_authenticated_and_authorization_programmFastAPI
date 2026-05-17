import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email, first_name, last_name, password, retry_password, is_admin, status_code",
    [
        ("kot1@pes.com", "kot1", "pes1", "1234", "1234", True, 200),
        ("kot2@pes.com", "kot2", "pes2", "1234", "1234", False, 200),
        ("kot1@pes.com", "kot", "pes", "1234", "1234", True, 409),
        ("abcde", "abc", "abc", "1234", "1234", True, 422),
        ("abcde@acbde", "abc", "abc", "1234", "1234", True, 422),
    ],
)
async def test_auth_flow(
    email: str,
    first_name: str,
    last_name: str,
    password: str,
    retry_password: str,
    is_admin: bool,
    status_code: int,
    ac: AsyncClient,
):
    # /register
    resp_register = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "retry_password": retry_password,
            "is_admin": is_admin,
        },
    )
    assert resp_register.status_code == status_code
    if status_code != 200:
        return

    resp_register2 = await ac.patch(
        "/auth/register",
        json={
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
        },
    )
    assert resp_register2.status_code == 422

    # /login
    resp_login = await ac.post(
        "/auth/login", json={"email": email, "password": password}
    )
    assert ac.cookies["access_token"]
    assert resp_register.status_code == status_code
    assert "access_token" in resp_login.cookies

    # /me
    resp_me = await ac.get("/auth/me")
    assert resp_register.status_code == status_code
    user = resp_me.json()
    assert "id" in user
    assert user["email"] == email
    assert "password" not in user
    assert "hashed_password" not in user

    # /logout
    resp_logout = await ac.post("/auth/logout")
    assert resp_register.status_code == status_code
    assert "access_token " not in resp_logout.cookies
