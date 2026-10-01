import random
import sys
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(ROOT / "backend")
)

from app.config import settings
from backend.app.models import Product
from app.database import Base


CATEGORIES = [
    "Electronics",
    "Computers",
    "Mobile",
    "Audio",
    "Gaming",
    "Home",
    "Kitchen",
    "Fitness",
    "Books",
    "Office",
]

BRANDS = [
    "Nova",
    "TechPro",
    "Vertex",
    "Apex",
    "Quantum",
    "Orion",
    "Zenith",
    "Pulse",
    "Core",
    "Atlas",
]


PRODUCT_TYPES = [
    "Laptop",
    "Phone",
    "Monitor",
    "Keyboard",
    "Mouse",
    "Headphones",
    "Camera",
    "Tablet",
    "Speaker",
    "Router",
]


def generate_products(count=100_000):

    products = []

    for i in range(1, count + 1):

        category = random.choice(
            CATEGORIES
        )

        brand = random.choice(
            BRANDS
        )

        product_type = random.choice(
            PRODUCT_TYPES
        )

        products.append(
            Product(
                name=(
                    f"{brand} "
                    f"{product_type} "
                    f"Model-{i}"
                ),
                category=category,
                brand=brand,
                price=round(
                    random.uniform(
                        20,
                        5000
                    ),
                    2
                ),
                stock=random.randint(
                    0,
                    1000
                )
            )
        )

    return products


def main():

    print(
        "Connecting to PostgreSQL..."
    )

    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True
    )

    Base.metadata.create_all(
        bind=engine
    )

    Session = sessionmaker(
        bind=engine
    )

    db = Session()

    try:

        existing = db.query(
            Product
        ).count()

        print(
            f"Existing products: {existing}"
        )

        if existing >= 100_000:

            print(
                "100,000 products already exist."
            )

            return

        products = generate_products(
            100_000 - existing
        )

        print(
            f"Generated {len(products)} products."
        )

        batch_size = 5_000

        for start in range(
            0,
            len(products),
            batch_size
        ):

            batch = products[
                start:start + batch_size
            ]

            db.bulk_save_objects(
                batch
            )

            db.commit()

            print(
                f"Inserted "
                f"{min(start + batch_size, len(products))}"
                f"/{len(products)}"
            )

        print(
            "Database seeding completed."
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()