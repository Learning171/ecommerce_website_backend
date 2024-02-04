from fastapi import APIRouter, Depends, HTTPException
from app.services.db_service import db_dependency
from app.services.order_services import create_order, get_order, get_orders
from app.validations.order_validations import OrderCreate

order_router = APIRouter(tags=["Orders"])


@order_router.post("/orders/")
def create_new_order(order_create: OrderCreate, db: db_dependency):
    return create_order(db, order_create)


@order_router.get("/orders/{order_id}")
def read_order(order_id: int, db: db_dependency):
    order = get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@order_router.get("/orders/")
def read_orders(db: db_dependency, skip: int = 0, limit: int = 10):
    return get_orders(db, skip=skip, limit=limit)
