from pydantic import BaseModel, UUID4


class LocationBase(BaseModel):
    longitude: float
    latitude: float

    class Config:
        from_attributes = True


class LocationOut(LocationBase):
    user_id: UUID4


class LocationInRedis(LocationOut):
    pass
