from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse
from ....src.models.tour_models import (
    Tour,
    TourDate,
    ItineraryItem,
    Booking,
    Traveler,
    Payment,
    Destination,
    Review,
    Category,
    Amenity,
)

from ....src.database.init_db import get_db
from ....src.schemas.tour_schemas import (
    BookingCreateSchema,
    BookingOutputSchema,
    BookingUpdateSchema,
    PaymentCreateSchema,
    PaymentOutputSchema,
    PaymentUpdateSchema,
    TourCreateSchema,
    TourOutputSchema,
    TourUpdateSchema,
    TourDateCreateSchema,
    TourDateOutputSchema,
    TourDateUpdateSchema,
    IntineraryCreateSchema,
    IntineraryOutputSchema,
    IntineraryUpdateSchema,
    DestinationCreateSchema,
    DestinationOutputSchema,
    DestinationUpdateSchema,
    ReviewCreateSchema,
    ReviewOutputSchema,
    ReviewUpdateSchema,
    CategoryCreateSchema,
    CategoryOutputSchema,
    CategoryUpdateSchema,
    AmenityCreateSchema,
    AmenityOutputSchema,
    AmenityUpdateSchema,
)


tour_router = APIRouter()




@tour_router.post("/destination", response_model=DestinationOutputSchema)
async def create_destination(
    request: DestinationCreateSchema, db: AsyncSession = Depends(get_db),current_user: Users = Depends(get_current_user)
):
    
    