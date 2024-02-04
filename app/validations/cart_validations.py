from pydantic import BaseModel, validator
from datetime import datetime
from typing import List
 
class CartBase(BaseModel):
    product_id: int
    user_id : int
    quantity: int
 
    @validator("quantity")
    def quantity_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Quantity must be positive")
        return value
 
class CartCreate(CartBase):
    pass
 
class CartResponse(CartBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
 
class CartList(BaseModel):
    items: List[CartResponse]
    total: int