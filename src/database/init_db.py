# type: ignore
from dotenv import load_dotenv
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession  # type: ignore
from .base_init import Base

# Import all models to register them with Base
from ..models.auth import Users  # noqa: F401 - needed to register models with Base
from ..models.tour_models import (
    Destination,
    Category,
    Amenity,
    Tour,
    TourDate,
    ItineraryItem,
    Booking,
    Traveler,
    Payment,
    Review,
)  # noqa: F401 - needed to register models with Base

# Load environment variables from .env file
load_dotenv()


# Load the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")


# Create an async engine
db_engine = create_async_engine(DATABASE_URL, future=True)


# Create an async session factory
async_session = async_sessionmaker(
    db_engine, expire_on_commit=False, class_=AsyncSession
)


# create a async session
async def get_db():
    async with async_session() as session:
        yield session


# Async function to create all tables
async def create_tables():
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
