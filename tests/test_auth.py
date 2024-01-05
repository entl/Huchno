from datetime import datetime

from .conftest import UserFactory, fake

from core.exceptions import PasswordDoesNotMatchException


async def test_Login_Success(async_client, session):
    data = {
        "username": fake.user_name(),
        "email": fake.ascii_email(),
        "password": "1233513tg",
        "fullname": "First Second",
        "birthdate": datetime.strftime(fake.date_of_birth(minimum_age=14, maximum_age=100), "%Y-%m-%d"),
    }

    await async_client.post("/users/", json=data)

    res = await async_client.post("/auth/login", data={"username": data["email"], "password": data["password"]})

    res_json = res.json()

    assert res.status_code == 200
    assert res_json["access_token"]


async def test_Login_InvalidPassword(async_client, session):
    user_factory = UserFactory(async_client=async_client, session=session)
    data = {
        "username": fake.user_name(),
        "email": fake.ascii_email(),
        "password": "1233513tg",
        "fullname": "First Second",
        "birthdate": datetime.strftime(fake.date_of_birth(minimum_age=14, maximum_age=100), "%Y-%m-%d"),
    }
    await user_factory.create_user(data)

    res = await async_client.post("/auth/login", data={"username": data["email"], "password": "wrong_password"})

    assert res.status_code == PasswordDoesNotMatchException.code
