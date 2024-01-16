from datetime import datetime

from starlette import status

from app.friends.models import Friendship
from app.friends.friendship_status_enum import FriendshipStatusEnum
from tests.conftest import UserFactory, fake


async def generate_sent_requests(from_user_id: str, to_user_ids: list[str], session):
    requests = []
    for i in range(len(to_user_ids)):
        requests.append(
            Friendship(requester_id=from_user_id, addressee_id=to_user_ids[i], status=FriendshipStatusEnum.sent.value)
        )
        requests.append(
            Friendship(requester_id=to_user_ids[i], addressee_id=from_user_id,
                       status=FriendshipStatusEnum.pending.value)
        )

    session.add_all(requests)
    await session.commit()
    await session.flush()
    return requests

async def generate_received_requests(from_user_ids: list[str], to_user_id: str, session):
    requests = []

    for i in range(len(from_user_ids)):
        requests.append(
            Friendship(requester_id=from_user_ids[i], addressee_id=to_user_id, status=FriendshipStatusEnum.sent.value)
        )
        requests.append(
            Friendship(requester_id=to_user_id, addressee_id=from_user_ids[i],
                       status=FriendshipStatusEnum.pending.value)
        )

    session.add_all(requests)
    await session.commit()
    await session.flush()
    return requests


async def test_GetSentRequests_Success(async_client, session):
    user_factory = UserFactory(async_client=async_client, session=session)
    users_data = [
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
    created_users = [await user_factory.create_user(user) for user in users_data]

    await generate_sent_requests(
        from_user_id=created_users[0]["id"],
        to_user_ids=[str(created_users[i]["id"]) for i in range(1, len(created_users))],
        session=session
    )

    authorized_client = user_factory.authorize_client(str(created_users[0]["id"]))
    res = await authorized_client.get("/friends/requests/sent")

    res_json = res.json()
    assert res.status_code == status.HTTP_200_OK
    # first user is requester, so we need to check only next ones
    assert len(res_json) == len(created_users[1:])


async def test_GetSentRequests_Unauthorized(async_client, session):
    res = await async_client.get("/friends/requests/sent")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


async def test_GetReceivedRequests_Success(async_client, session):
    user_factory = UserFactory(async_client=async_client, session=session)
    users_data = [
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
    created_users = [await user_factory.create_user(user) for user in users_data]

    await generate_received_requests(
        from_user_ids=[str(created_users[i]["id"]) for i in range(1, len(created_users))],
        to_user_id=created_users[0]["id"],
        session=session
    )

    authorized_client = user_factory.authorize_client(str(created_users[0]["id"]))
    res = await authorized_client.get("/friends/requests/received")

    res_json = res.json()
    assert res.status_code == status.HTTP_200_OK
    # first user is addressee, so we need to check only next ones
    assert len(res_json) == len(created_users[1:])


async def test_GetReceivedRequests_Unauthorized(async_client, session):
    res = await async_client.get("/friends/requests/received")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
