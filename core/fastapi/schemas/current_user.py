from pydantic import BaseModel, Field, UUID4


class CurrentUser(BaseModel):
    id: UUID4 = Field(None, description="ID")
    permissions: list[str] = Field(None, description="Permissions")

    class Config:
        validate_assignment = True
