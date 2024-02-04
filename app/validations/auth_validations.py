from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from typing import List

class UserRole(str, Enum):
    admin = 'admin'
    customer = 'customer'
    shop_owner = 'shop_owner'

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.customer

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    is_active: Optional[bool] = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class TokenData(BaseModel):
    email: str | None = None

class AddressBase(BaseModel):
    user_id: int
    street: str
    city: str
    state: str
    zip_code: str

class AddressCreate(AddressBase):
    pass

class AddressResponse(AddressBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

class AddressList(BaseModel):
    items: List[AddressResponse]
    total: int
