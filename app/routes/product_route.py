from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.db_service import db_dependency
from app.services.product_services import (
    get_all_products,
    get_products_by_category,
    create_product,
    update_product,
    delete_product,
)
from app.validations.product_validations import ProductCreate, ProductCategory

product_router = APIRouter(tags=["Products"])


@product_router.get("/products/")
def read_all_products(db: db_dependency, skip: int = 0, limit: int = 10):
    products = get_all_products(db, skip=skip, limit=limit)
    return products


@product_router.get("/products/category/{category}")
def read_products_by_category(
    category: ProductCategory,
    db: db_dependency,
    skip: int = 0,
    limit: int = 10,
):
    products = get_products_by_category(db, category, skip=skip, limit=limit)
    return products


@product_router.post("/products/")
def create_new_product(product_create: ProductCreate, db: db_dependency):
    return create_product(db, product_create)


@product_router.put("/products/{product_id}")
def update_existing_product(
    product_id: int, product_update: ProductCreate, db: db_dependency
):
    updated_product = update_product(db, product_id, product_update)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@product_router.delete("/products/{product_id}")
def delete_existing_product(product_id: int, db: db_dependency):
    product = delete_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
