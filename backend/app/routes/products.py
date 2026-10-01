from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.product import Product


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/")
def get_products(
    limit: int = Query(
        default=50,
        ge=1,
        le=500
    ),
    offset: int = Query(
        default=0,
        ge=0
    ),
    db: Session = Depends(get_db)
):

    products = (
        db.query(Product)
        .order_by(Product.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return [
        {
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "brand": product.brand,
            "price": product.price,
            "stock": product.stock
        }
        for product in products
    ]


@router.get("/search")
def search_products(
    q: str = Query(
        min_length=1,
        max_length=100
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=500
    ),
    db: Session = Depends(get_db)
):

    products = (
        db.query(Product)
        .filter(
            Product.name.ilike(
                f"%{q}%"
            )
        )
        .limit(limit)
        .all()
    )

    return [
        {
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "brand": product.brand,
            "price": product.price,
            "stock": product.stock
        }
        for product in products
    ]


@router.get("/summary")
def product_summary(
    db: Session = Depends(get_db)
):

    result = db.query(
        func.count(Product.id).label(
            "total_products"
        ),
        func.avg(Product.price).label(
            "average_price"
        ),
        func.sum(Product.stock).label(
            "total_stock"
        )
    ).first()

    return {
        "total_products": result.total_products,
        "average_price": round(
            float(result.average_price or 0),
            2
        ),
        "total_stock": result.total_stock
    }


@router.get("/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = (
        db.query(Product)
        .filter(
            Product.id == product_id
        )
        .first()
    )

    if not product:
        return {
            "error": "Product not found"
        }

    return {
        "id": product.id,
        "name": product.name,
        "category": product.category,
        "brand": product.brand,
        "price": product.price,
        "stock": product.stock
    }