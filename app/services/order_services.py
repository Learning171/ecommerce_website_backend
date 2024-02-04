from app.services.db_service import db_dependency
from app.models.order_model import Order
from app.validations.order_validations import OrderCreate


def create_order(db: db_dependency, order_create: OrderCreate):
    db_order = Order(**order_create.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: db_dependency, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders(db: db_dependency, skip: int = 0, limit: int = 10):
    return db.query(Order).offset(skip).limit(limit).all()
