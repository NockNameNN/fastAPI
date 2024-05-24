from pydantic import BaseModel, ConfigDict


class RoleUserBase(BaseModel):
    user_id: int
    role_id: int


class RoleUserCreate(RoleUserBase):
    pass


class RoleUser(RoleUserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class RoleUserUpdate(RoleUserBase):
    user_id: int = None
    role_id: int = None
