from pydantic import BaseModel, validator
from datetime import datetime
from enum import Enum
from typing import List, Optional


class ProductSubcategory(str, Enum):
    SUBCATEGORY1 = "Subcategory 1"
    SUBCATEGORY2 = "Subcategory 2"


class ProductCategory(str, Enum):
    ELECTRONICS = "Electronics"
    CLOTHING = "Clothing"
    BOOKS = "Books"
    TOYS = "Toys"
    OTHER = "Other"


class ProductBase(BaseModel):
    name: str
    image: str
    category: ProductCategory
    subcategory: Optional[ProductSubcategory]
    description: str
    price: float
    stock_quantity: int
    rating: Optional[int]
    seller_id: int

    @validator("price")
    def price_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Price must be positive")
        return value

    @validator("stock_quantity")
    def stock_quantity_must_be_non_negative(cls, value):
        if value < 0:
            raise ValueError("Stock quantity must be non-negative")
        return value


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool


class ProductList(BaseModel):
    items: List[ProductResponse]
    total: int
