from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.db_config import Base
from app.validations.product_validations import ProductCategory, ProductSubcategory


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(Enum(ProductCategory), index=True)
    subcategory = Column(Enum(ProductSubcategory), nullable=True)
    description = Column(String)
    image = Column(String)
    price = Column(Float)
    stock_quantity = Column(Integer)
    rating = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    seller_id = Column(Integer, ForeignKey("users.id"))
    seller = relationship("User", back_populates="products")
    orders = relationship("Order", back_populates="product")
    cart_items = relationship("Cart", back_populates="product")
    reviews = relationship("Review", back_populates="product")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    rating = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="reviews")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="reviews")
