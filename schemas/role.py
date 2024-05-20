from pydantic import BaseModel, ConfigDict


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class RoleUpdate(RoleBase):
    name: str = None
