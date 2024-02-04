# from fastapi import APIRouter, Depends, HTTPException, status
# from app.services.db_service import db_dependency
# from app.models.auth_model import User
# from app.validations.auth_validations import UserCreate, TokenData, UserResponse, UserRole
# from jose import JWTError, jwt
# from datetime import datetime, timedelta
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from passlib.context import CryptContext
# from app.services.utils import send_password_reset_email


# auth_router = APIRouter(tags=["Auth"])

# SECRET_KEY = "Abc1abc2"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # Password hashing context
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# # Function to create access token
# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# def verify_token(token:str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could Not Validate credentials",
#         headers={"WWW-Authenticate" : "Bearer"}
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except JWTError:
#         raise credentials_exception

# def get_current_user_role(current_user:dict = Depends(verify_token)):
#     return current_user.get("role")

# # Dependency to check if the user has admin privileges
# def check_admin_privilege(role: str = Depends(get_current_user_role)):
#     if role != UserRole.admin:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privilege required")
#     return role
 
# # Dependency to check if the user has shop owner privileges
# def check_shop_owner_privilege(role: str = Depends(get_current_user_role)):
#     if role != UserRole.shop:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Shop owner privilege required")
#     return role

# # Dependency to check if the user has shop owner privileges
# def check_customer_privilege(role: str = Depends(get_current_user_role)):
#     if role != UserRole.customer:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Customer privilege required")
#     return role

# # Function to verify password
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def get_user(db:db_dependency, username: str):
#     return db.query(User).filter(User.username == username).first()

# # Function to get current user from token
# async def get_current_user(db:db_dependency, token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(db, username=token_data.username)
#     if user is None:
#         raise credentials_exception 


#     return user


# # Function to get current active user
# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if not current_user.is_active:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
#                             detail="Inactive user",
#                             headers={"WWW-Authenticate": "Bearer"}
#                             )
#     return current_user

# # Function to generate password reset token
# def generate_password_reset_token(email: str) -> str:
#     expire_time = datetime.utcnow() + timedelta(minutes=30)
#     to_encode = {"sub": email, "exp": expire_time}
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# @auth_router.post("/register")
# def register_user(db: db_dependency, user: UserCreate):
#     existing_user = db.query(User).filter(User.email == user.email).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Username or email already registered")
#     hashed_password = pwd_context.hash(user.hashed_password)
#     new_user = User(
#         username=user.username,
#         email=user.email,
#         hashed_password=hashed_password,
#         role=user.role,
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return {"message": "User registered successfully", "user_id": new_user.id}

# @auth_router.post("/login")
# def login_user(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
#     user = db.query(User).filter(User.username == form_data.username).first()

#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# @auth_router.get("/profile", response_model=UserResponse)
# def get_user_profile(current_user: User = Depends(get_current_active_user)):
#     return current_user

# @auth_router.put("/change-password")
# def change_user_password(
#     db: db_dependency,
#     new_password: str,
#     current_user: User = Depends(get_current_user)
# ):
#     if not verify_password(new_password, current_user.hashed_password):
#         raise HTTPException(
#             status_code=400,
#             detail="Invalid current password",
#         )
#     hashed_password = pwd_context.hash(new_password)
#     current_user.hashed_password = hashed_password
#     db.commit()

#     return {"message": "Password changed successfully"}

# @auth_router.post("/reset-password-mail")
# def send_password_reset_mail(db: db_dependency, email: str):
#     user = db.query(User).filter(User.email == email).first()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     reset_token = generate_password_reset_token(user.email)
#     reset_link = f"http://localhost:3000/reset-password?token={reset_token}"

#     send_password_reset_email(email, reset_link) 

#     return {"message": "Password reset email sent successfully"}
# ###########################################################################################

# from fastapi import APIRouter, Depends
# from app.services.db_service import db_dependency
# from app.models.product_model import Product
# from app.validations.product_validations import (
#     ProductCreate,
#     ProductResponse
# )
# from typing import Annotated
# from app.routes.auth_routes import (
#     check_admin_privilege,
#     check_shop_owner_privilege,
#     check_customer_privilege,
# )

# admin_required = Annotated[str, Depends(check_admin_privilege)]
# shop_owner_required = Annotated[str, Depends(check_shop_owner_privilege)]
# cutomer_required = Annotated[str, Depends(check_customer_privilege)]


# product_router = APIRouter(tags=["Products"])


# @product_router.post("/products/", response_model=ProductResponse)
# def create_product(
#     product: ProductCreate,
#     user: cutomer_required | shop_owner_required | admin_required,
#     db: db_dependency,
# ):
#     db_product = Product(**product.dict())
#     db.add(db_product)
#     db.commit()
#     db.refresh(db_product)
#     return db_product

#################################################################################

# from fastapi import APIRouter, Depends, HTTPException
# from app.services.db_service import db_dependency
# from app.models.product_model import Product, Category
# from app.validations.product_validations import (
#     ProductCreate,
#     ProductResponse,
#     CategoryCreate,
#     CategoryResponse,
#     ProductList,
#     CategoryList,
# )
# from typing import Annotated
# from app.routes.auth_routes import (
#     check_admin_or_customer,
#     check_shop_owner_privilege
# )

# shop_owner_required = Annotated[str, Depends(check_shop_owner_privilege)]
# admin_or_customer_required = Annotated[str, Depends(check_admin_or_customer)]


# product_router = APIRouter(tags=["Products"])
# category_router = APIRouter(tags=["Category"])


# @product_router.post("/products/")
# def create_product(
#     product: ProductCreate,
#     category_name : str,
#     user: shop_owner_required,
#     db: db_dependency,
# ):
#     # category = db.query(Category).filter(Category.name == category_name).first()
#     db_product = Product(**product.dict())
#     db.add(db_product)
#     db.commit()
#     db.refresh(db_product)
#     return db_product


# @product_router.get("/products/{product_id}")
# def read_product(
#     product_id: int,
#     category_name : str,
#     user: admin_or_customer_required,
#     db: db_dependency,
# ):
#     # category_data = [category_name]
#     db_product = db.query(Product).filter(Product.id == product_id).first()
#     if db_product is None:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return db_product

# @product_router.get("/products/")
# def list_products(
#     user: admin_or_customer_required, 
#     db: db_dependency
# ):
#     products = db.query(Product).all()
#     total = db.query(Product).count()
#     return {"items": products, "total": total}

# @product_router.put("/products/{product_id}")
# def update_product(
#     product_id: int,
#     user: shop_owner_required,
#     product: ProductCreate,
#     db: db_dependency,
# ):
#     db_product = db.query(Product).filter(Product.id == product_id).first()
#     if db_product is None:
#         raise HTTPException(status_code=404, detail="Product not found")

#     for key, value in product.dict().items():
#         setattr(db_product, key, value)

#     db.commit()
#     db.refresh(db_product)
#     return db_product


# @product_router.delete("/products/{product_id}")
# def delete_product(
#     product_id: int,
#     user: shop_owner_required,
#     db: db_dependency,
# ):
#     db_product = db.query(Product).filter(Product.id == product_id).first()
#     if db_product is None:
#         raise HTTPException(status_code=404, detail="Product not found")

#     db.delete(db_product)
#     db.commit()
#     return db_product

# # Category routes

# @category_router.post("/categories/")
# def create_category(
#     category: CategoryCreate,
#     user: shop_owner_required,
#     db: db_dependency,
# ):
#     db_category = Category(**category.dict())
#     db.add(db_category)
#     db.commit()
#     db.refresh(db_category)
#     return db_category


# @category_router.get("/categories/{category_id}")
# def read_category(
#     category_id: int,
#     user: admin_or_customer_required,
#     db: db_dependency,
# ):
#     db_category = db.query(Category).filter(Category.id == category_id).first()
#     if db_category is None:
#         raise HTTPException(status_code=404, detail="Category not found")
#     return db_category

# @category_router.get("/categories/")
# def list_categories(
#     user: admin_or_customer_required,
#     db: db_dependency
# ):
#     categories = db.query(Category).all()
#     total = db.query(Category).count()
#     return {"items": categories, "total": total}

# @category_router.put("/categories/{category_id}")
# def update_category(
#     category_id: int,
#     category: CategoryCreate,
#     user: shop_owner_required,
#     db: db_dependency,
# ):
#     db_category = db.query(Category).filter(Category.id == category_id).first()
#     if db_category is None:
#         raise HTTPException(status_code=404, detail="Category not found")

#     for key, value in category.dict().items():
#         setattr(db_category, key, value)

#     db.commit()
#     db.refresh(db_category)
#     return db_category


# @category_router.delete("/categories/{category_id}")
# def delete_category(
#     category_id: int,
#     user: shop_owner_required,
#     db: db_dependency,
# ):
#     db_category = db.query(Category).filter(Category.id == category_id).first()
#     if db_category is None:
#         raise HTTPException(status_code=404, detail="Category not found")

#     db.delete(db_category)
#     db.commit()
#     return db_category
##########################################################################################################

from pydantic import BaseModel
from datetime import datetime
from typing import List

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock_quantity: int

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

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

class CategoryList(BaseModel):
    items: List[CategoryResponse]
    total: int


from pydantic import BaseModel, validator
from datetime import datetime
from typing import List

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock_quantity: int

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

class CategoryBase(BaseModel):
    name: str

    @validator("name")
    def name_must_not_be_blank(cls, value):
        if not value.strip():
            raise ValueError("Category name cannot be blank")
        return value

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

class CategoryList(BaseModel):
    items: List[CategoryResponse]
    total: int

class ReviewBase(BaseModel):
    content: str
    rating: float

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

class RatingBase(BaseModel):
    rating: float

    @validator("rating")
    def rating_must_be_in_range(cls, value):
        if not (0 <= value <= 5):
            raise ValueError("Rating must be between 0 and 5")
        return value

class RatingCreate(RatingBase):
    pass

class RatingResponse(RatingBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

class RatingList(BaseModel):
    items: List[RatingResponse]
    total: int


from typing import List

from sqlalchemy.orm import Session
from app.models import Product, Category, Review, Rating
from app.schemas import (
    ProductCreate, ProductResponse, ProductList,
    CategoryCreate, CategoryResponse, CategoryList,
    ReviewCreate, ReviewResponse, ReviewList,
    RatingCreate, RatingResponse, RatingList
)

# Products
def create_product(db: Session, product_create: ProductCreate):
    db_product = Product(**product_create.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 10):
    products = db.query(Product).offset(skip).limit(limit).all()
    total = db.query(Product).count()
    return ProductList(items=products, total=total)

# Categories
def create_category(db: Session, category_create: CategoryCreate):
    db_category = Category(**category_create.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 10):
    categories = db.query(Category).offset(skip).limit(limit).all()
    total = db.query(Category).count()
    return CategoryList(items=categories, total=total)

# Reviews
def create_review(db: Session, review_create: ReviewCreate):
    db_review = Review(**review_create.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_review(db: Session, review_id: int):
    return db.query(Review).filter(Review.id == review_id).first()

def get_reviews(db: Session, skip: int = 0, limit: int = 10):
    reviews = db.query(Review).offset(skip).limit(limit).all()
    total = db.query(Review).count()
    return ReviewList(items=reviews, total=total)

# Ratings
def create_rating(db: Session, rating_create: RatingCreate):
    db_rating = Rating(**rating_create.dict())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def get_rating(db: Session, rating_id: int):
    return db.query(Rating).filter(Rating.id == rating_id).first()

def get_ratings(db: Session, skip: int = 0, limit: int = 10):
    ratings = db.query(Rating).offset(skip).limit(limit).all()
    total = db.query(Rating).count()
    return RatingList(items=ratings, total=total)



from sqlalchemy.orm import Session
from app.models import Product, Category
from app.schemas import ProductCreate, ProductResponse, ProductList

class ProductService:
    @staticmethod
    def create_product(db: Session, product_create: ProductCreate):
        product = Product(**product_create.dict())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def get_products(db: Session, skip: int = 0, limit: int = 10):
        products = db.query(Product).offset(skip).limit(limit).all()
        total = db.query(Product).count()
        return ProductList(items=[ProductResponse.from_orm(product) for product in products], total=total)

    @staticmethod
    def get_product(db: Session, product_id: int):
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def update_product(db: Session, product_id: int, product_update: ProductCreate):
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            for key, value in product_update.dict().items():
                setattr(product, key, value)
            db.commit()
            db.refresh(product)
        return product

    @staticmethod
    def delete_product(db: Session, product_id: int):
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            db.delete(product)
            db.commit()
        return product

    @staticmethod
    def assign_category_to_product(db: Session, product_id: int, category_id: int):
        product = db.query(Product).filter(Product.id == product_id).first()
        category = db.query(Category).filter(Category.id == category_id).first()

        if product and category:
            product.categories.append(category)
            db.commit()
            db.refresh(product)

        return product



from sqlalchemy.orm import Session
from app.models import Product, ProductCreate, ProductResponse

def create_product(db: Session, product_create: ProductCreate):
    db_product = Product(**product_create.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Product).offset(skip).limit(limit).all()

def update_product(db: Session, product_id: int, product_update: ProductCreate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    for key, value in product_update.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    db.delete(db_product)
    db.commit()
    return db_product

# Additional services can include retrieving products based on specific criteria, handling relationships with categories, reviews, etc.



from sqlalchemy.orm import Session
from app.models import Category, CategoryCreate, CategoryResponse

def create_category(db: Session, category_create: CategoryCreate):
    db_category = Category(**category_create.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Category).offset(skip).limit(limit).all()

def update_category(db: Session, category_id: int, category_update: CategoryCreate):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    for key, value in category_update.dict().items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    db.delete(db_category)
    db.commit()
    return db_category


from sqlalchemy.orm import Session
from app.models import Review, ReviewCreate, ReviewResponse

def create_review(db: Session, review_create: ReviewCreate):
    db_review = Review(**review_create.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_review(db: Session, review_id: int):
    return db.query(Review).filter(Review.id == review_id).first()

def get_reviews(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Review).offset(skip).limit(limit).all()

def update_review(db: Session, review_id: int, review_update: ReviewCreate):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    for key, value in review_update.dict().items():
        setattr(db_review, key, value)
    db.commit()
    db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: int):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    db.delete(db_review)
    db.commit()
    return db_review



from sqlalchemy.orm import Session
from app.models import Rating, RatingCreate, RatingResponse

def create_rating(db: Session, rating_create: RatingCreate):
    db_rating = Rating(**rating_create.dict())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def get_rating(db: Session, rating_id: int):
    return db.query(Rating).filter(Rating.id == rating_id).first()

def get_ratings(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Rating).offset(skip).limit(limit).all()

def update_rating(db: Session, rating_id: int, rating_update: RatingCreate):
    db_rating = db.query(Rating).filter(Rating.id == rating_id).first()
    for key, value in rating_update.dict().items():
        setattr(db_rating, key, value)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def delete_rating(db: Session, rating_id: int):
    db_rating = db.query(Rating).filter(Rating.id == rating_id).first()
    db.delete(db_rating)
    db.commit()
    return db_rating


from sqlalchemy.orm import Session
from app.models import Product, ProductCreate, ProductResponse

def create_product(db: Session, product_create: ProductCreate):
    db_product = Product(**product_create.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Product).offset(skip).limit(limit).all()

def update_product(db: Session, product_id: int, product_update: ProductCreate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    for key, value in product_update.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    db.delete(db_product)
    db.commit()
    return db_product


from sqlalchemy.orm import Session
from app.models import Category, CategoryCreate, CategoryResponse

def create_category(db: Session, category_create: CategoryCreate):
    db_category = Category(**category_create.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Category).offset(skip).limit(limit).all()

def update_category(db: Session, category_id: int, category_update: CategoryCreate):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    for key, value in category_update.dict().items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    db.delete(db_category)
    db.commit()
    return db_category


from sqlalchemy.orm import Session
from app.models import Review, ReviewCreate, ReviewResponse, Rating, RatingCreate, RatingResponse

def create_review(db: Session, review_create: ReviewCreate):
    db_review = Review(**review_create.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_review(db: Session, review_id: int):
    return db.query(Review).filter(Review.id == review_id).first()

def get_reviews(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Review).offset(skip).limit(limit).all()

def create_rating(db: Session, rating_create: RatingCreate):
    db_rating = Rating(**rating_create.dict())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def get_rating(db: Session, rating_id: int):
    return db.query(Rating).filter(Rating.id == rating_id).first()

def get_ratings(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Rating).offset(skip).limit(limit).all()



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.review_service import create_review, get_review, get_reviews
from app.services.rating_service import create_rating, get_rating, get_ratings
from app.models import ReviewCreate, ReviewResponse, RatingCreate, RatingResponse

router = APIRouter()

# Review Endpoints
@router.post("/reviews/", response_model=ReviewResponse)
def create_new_review(review_create: ReviewCreate, db: Session = Depends(get_db)):
    return create_review(db, review_create)

@router.get("/reviews/{review_id}", response_model=ReviewResponse)
def read_review(review_id: int, db: Session = Depends(get_db)):
    review = get_review(db, review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.get("/reviews/", response_model=list[ReviewResponse])
def read_reviews(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_reviews(db, skip=skip, limit=limit)

# Rating Endpoints
@router.post("/ratings/", response_model=RatingResponse)
def create_new_rating(rating_create: RatingCreate, db: Session = Depends(get_db)):
    return create_rating(db, rating_create)

@router.get("/ratings/{rating_id}", response_model=RatingResponse)
def read_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = get_rating(db, rating_id)
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating

@router.get("/ratings/", response_model=list[RatingResponse])
def read_ratings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_ratings(db, skip=skip, limit=limit)



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.category_service import create_category, get_category, get_categories, update_category, delete_category
from app.models import CategoryCreate, CategoryResponse

router = APIRouter()

@router.post("/categories/", response_model=CategoryResponse)
def create_new_category(category_create: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, category_create)

@router.get("/categories/{category_id}", response_model=CategoryResponse)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/categories/", response_model=list[CategoryResponse])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_categories(db, skip=skip, limit=limit)

@router.put("/categories/{category_id}", response_model=CategoryResponse)
def update_existing_category(category_id: int, category_update: CategoryCreate, db: Session = Depends(get_db)):
    category = update_category(db, category_id, category_update)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/categories/{category_id}", response_model=CategoryResponse)
def delete_existing_category(category_id: int, db: Session = Depends(get_db)):
    category = delete_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.product_service import create_product, get_product, get_products, update_product, delete_product
from app.models import ProductCreate, ProductResponse

router = APIRouter()

@router.post("/products/", response_model=ProductResponse)
def create_new_product(product_create: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product_create)

@router.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/products/", response_model=list[ProductResponse])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_products(db, skip=skip, limit=limit)

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_existing_product(product_id: int, product_update: ProductCreate, db: Session = Depends(get_db)):
    product = update_product(db, product_id, product_update)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    product = delete_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
