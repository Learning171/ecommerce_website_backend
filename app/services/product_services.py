from app.services.db_service import db_dependency
from fastapi import UploadFile
from app.models.product_model import Product
from app.validations.product_validations import ProductCreate
from app.validations.product_validations import ProductCategory


def get_all_products(db: db_dependency, skip: int = 0, limit: int = 10):
    return db.query(Product).offset(skip).limit(limit).all()


def get_products_by_category(
    db: db_dependency, category: ProductCategory, skip: int = 0, limit: int = 10
):
    return (
        db.query(Product)
        .filter(Product.category == category)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_product(db: db_dependency, product_create: ProductCreate):
    db_product = Product(**product_create.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: db_dependency, product_id: int, product_update: ProductCreate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        for key, value in product_update.dict().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: db_dependency, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product


# def save_product_image(upload_file: UploadFile):
#     file_extension = upload_file.filename.split(".")[-1]
#     file_name = f"{uuid4()}.{file_extension}"
#     file_path = os.path.join("app/images", file_name)

#     with open(file_path, "wb") as file:
#         file.write(upload_file.file.read())

#     return file_name
