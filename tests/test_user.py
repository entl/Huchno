from datetime import datetime, date

from app.user import schemas as user_schemas
from core.exceptions import UserAgeInvalid
from .conftest import fake


async def test_CreateUser_Success(async_client):
    data = {
        "username": fake.user_name(),
        "email": fake.ascii_email(),
        "password": "1233513tg",
        "fullname": "First Second",
        "birthdate": datetime.strftime(fake.date_of_birth(minimum_age=14, maximum_age=100), "%Y-%m-%d"),
    }
    res = await async_client.post("/users/",
                                  json=data)
    res_schema = user_schemas.UserOut(**res.json())
    assert res_schema.username == data['username']
    assert res_schema.fullname == data['fullname']
    assert res_schema.birthdate == datetime.strptime(data['birthdate'], "%Y-%m-%d").date()
    assert not res_schema.verified
    assert not res_schema.last_login
    assert res_schema.registration_date == date.today()


async def test_CreateUser_AgeInvalid(async_client):
    data = {
        "username": "test",
        "email": "test_email@gmail.com",
        "password": "1233513tg",
        "fullname": "First Second",
        "birthdate": "2020-03-03",
    }

    res = await async_client.post("/users/",
                                  json=data)

    res_json = res.json()
    assert res.status_code == UserAgeInvalid.code
    assert res_json["error_code"] == UserAgeInvalid.error_code

