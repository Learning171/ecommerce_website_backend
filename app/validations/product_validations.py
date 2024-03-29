from pydantic import BaseModel, Field
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
    category: ProductCategory
    subcategory: Optional[ProductSubcategory]
    description: str
    price: float = Field(gt=0)
    stock_quantity: int = Field(gt=0)
    rating: Optional[int]
    seller_id: int

class ImageBase(BaseModel):
    url: str


class ImageCreate(ImageBase):
    pass


class ImageResponse(ImageBase):
    id: int
    product_id: int


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    image: ImageBase


class ProductList(BaseModel):
    items: List[ProductResponse]
    total: int
