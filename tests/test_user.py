from datetime import datetime, date

from starlette import status

from app.user import schemas as user_schemas
from core.exceptions import UserAgeInvalid, DuplicateEmailOrNicknameException
from .conftest import fake, UserFactory


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


async def test_CreateUser_UsernameDuplicate(async_client):
    data = {
        "username": "test",
        "email": fake.ascii_email(),
        "password": "1233513tg",
        "fullname": "First Second",
        "birthdate": datetime.strftime(fake.date_of_birth(minimum_age=14, maximum_age=100), "%Y-%m-%d"),
    }

    await async_client.post("/users/", json=data)

    data = {
        "username": "test",
        "email": fake.ascii_email(),
        "password": "1233513tg",
        "fullname": "First Second",
        "birthdate": datetime.strftime(fake.date_of_birth(minimum_age=14, maximum_age=100), "%Y-%m-%d"),
    }

    res = await async_client.post("/users/", json=data)

    res_json = res.json()
    assert res.status_code == DuplicateEmailOrNicknameException.code
    assert res_json["error_code"] == DuplicateEmailOrNicknameException.error_code


async def test_CreateUser_EmailDuplicate(async_client):
    data = {
        "username": fake.user_name(),
        "email": "test@gmail.com",
        "password": "1233513tg",
        "fullname": "First Second",
        "birthdate": datetime.strftime(fake.date_of_birth(minimum_age=14, maximum_age=100), "%Y-%m-%d"),
    }

    await async_client.post("/users/", json=data)

    data = {
        "username": fake.user_name(),
        "email": "test@gmail.com",
        "password": "1233513tg",
        "fullname": "First Second",
        "birthdate": datetime.strftime(fake.date_of_birth(minimum_age=14, maximum_age=100), "%Y-%m-%d"),
    }

    res = await async_client.post("/users/", json=data)

    res_json = res.json()
    assert res.status_code == DuplicateEmailOrNicknameException.code
    assert res_json["error_code"] == DuplicateEmailOrNicknameException.error_code


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


async def test_CreateUser_SchemaInvalid(async_client):
    data = {
        "username": "",
        "email": "",
        "password": "",
        "fullname": "",
        "birthdate": None,
    }

    res = await async_client.post("/users/", json=data)

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_GetAllUsers_Successful(async_client, session):
    user_factory = UserFactory(async_client=async_client, session=session)
    data = [
        {
            "username": fake.user_name(),
            "email": fake.ascii_email(),
            "password": fake.password(length=10),
            "fullname": fake.name(),
            "birthdate": datetime.strftime(fake.date_of_birth(minimum_age=14, maximum_age=100), "%Y-%m-%d"),
        },
        {
            "username": fake.user_name(),
            "email": fake.ascii_email(),
            "password": fake.password(length=10),
            "fullname": fake.name(),
            "birthdate": datetime.strftime(fake.date_of_birth(minimum_age=14, maximum_age=100), "%Y-%m-%d"),
        },
        {
            "username": fake.user_name(),
            "email": fake.ascii_email(),
            "password": fake.password(length=10),
            "fullname": fake.name(),
            "birthdate": datetime.strftime(fake.date_of_birth(minimum_age=14, maximum_age=100), "%Y-%m-%d"),
        }
    ]
    created_clients = [await user_factory.create_user(user) for user in data]
    authorized_client = user_factory.authorize_client(str(created_clients[0]["id"]))

    res = await authorized_client.get("/users/")
    assert res.status_code == status.HTTP_200_OK


async def test_GetAllUsers_Unauthorized(async_client, session):
    res = await async_client.get("/users/")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

