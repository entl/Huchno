from pydantic import BaseModel, Field, UUID4


class CurrentUser(BaseModel):
    id: UUID4 = Field(None, description="ID")

    class Config:
        validate_assignment = True
