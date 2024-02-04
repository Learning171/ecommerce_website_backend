from pydantic import BaseModel, validator
from datetime import datetime
from typing import List


class ReviewBase(BaseModel):
    content: str
    rating: float
    product_id: int
    user_id: int

    @validator("rating")
    def rating_must_be_in_range(cls, value):
        if not (0 <= value <= 5):
            raise ValueError("Rating must be between 0 and 5")
        return value


class ReviewCreate(ReviewBase):
    pass


class ReviewResponse(ReviewBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool


class ReviewList(BaseModel):
    items: List[ReviewResponse]
    total: int
