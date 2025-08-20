from datetime import datetime
from ..database.base_init import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table, func


tour_amenities = Table(
    "tour_amenities",
    Base.metadata,
    Column("tour_id", Integer, ForeignKey("tours.id"), primary_key=True),
    Column("amenity_id", Integer, ForeignKey("amenities.id"), primary_key=True),
)


tour_categories = Table(
    "tour_categories",
    Base.metadata,
    Column("tour_id", Integer, ForeignKey("tours.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
)

booking_travelers = Table(
    "booking_travelers",
    Base.metadata,
    Column("booking_id", Integer, ForeignKey("bookings.id"), primary_key=True),
    Column("traveler_id", Integer, ForeignKey("travelers.id"), primary_key=True),
)


class Destination(Base):
    __tablename__ = "destinations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    tours = relationship("Tour", back_populates="destination")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    tours = relationship("Tour", back_populates="categories")


class Amenity(Base):
    __tablename__ = "amenities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    tours = relationship("Tour", back_populates="amenities")


class Tour(Base):
    __tablename__ = "tours"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    short_description: Mapped[str] = mapped_column(String(500), nullable=False)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    duration_nights: Mapped[int] = mapped_column(Integer, nullable=False)
    max_participants: Mapped[int] = mapped_column(Integer, nullable=False)
    min_participants: Mapped[int] = mapped_column(Integer, default=1)
    price_per_person: Mapped[float] = mapped_column(nullable=False)
    discount_percentage: Mapped[float] = mapped_column(default=0.0)
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    is_featured: Mapped[bool] = mapped_column(default=False)

    destionation_id: Mapped[int] = mapped_column(
        ForeignKey("destinations.id"), nullable=False
    )

    destination = relationship("Destination", back_populates="tours")

    categories = relationship(
        "Category", secondary=tour_categories, back_populates="tours"
    )

    amenities = relationship(
        "Amenity", secondary=tour_amenities, back_populates="tours"
    )

    tour_dates = relationship("TourDate", back_populates="tour")
    bookings = relationship("Booking", back_populates="tour")
    reviews = relationship("Review", back_populates="tour")
    itinerarY_items = relationship("ItineraryItem", back_populates="tour")


class TourDate(Base):
    __tablename__ = "tour_dates"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    start_date: Mapped[datetime] = mapped_column(nullable=False)
    end_date: Mapped[datetime] = mapped_column(nullable=False)
    tour_id: Mapped[int] = mapped_column(ForeignKey("tours.id"), nullable=False)

    available_spots: Mapped[int] = mapped_column(Integer, nullable=False)
    price_per_person: Mapped[float] = mapped_column(nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    is_active: Mapped[bool] = mapped_column(default=True)

    tour = relationship("Tour", back_populates="tour_dates")
    bookings = relationship("Booking", back_populates="tour_date")


class ItineraryItem(Base):
    __tablename__ = "itinerary_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    day_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    activities: Mapped[str] = mapped_column(String(1000), nullable=True)
    meals_included: Mapped[str] = mapped_column(String(100), nullable=True)
    accommodation: Mapped[str] = mapped_column(String(200), nullable=True)

    tour_id: Mapped[int] = mapped_column(ForeignKey("tours.id"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    tour = relationship("Tour", back_populates="itinerary_items")


class Traveler(Base):
    __tablename__ = "travelers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user = relationship("Users", back_populates="travelers")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    bookings = relationship(
        "Booking", secondary=booking_travelers, back_populates="travelers"
    )


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    booking_reference: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    number_of_travelers: Mapped[int] = mapped_column(Integer, nullable=False)
    total_amount: Mapped[float] = mapped_column(nullable=False)
    payment_status: Mapped[str] = mapped_column(String(50), default="pending")
    booking_status: Mapped[str] = mapped_column(String(50), default="confirmed")
    special_requests: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    tour_id: Mapped[int] = mapped_column(ForeignKey("tours.id"), nullable=False)
    tour_date_id: Mapped[int] = mapped_column(
        ForeignKey("tour_dates.id"), nullable=False
    )

    user = relationship("Users", back_populates="bookings")
    tour = relationship("Tour", back_populates="bookings")
    tour_date = relationship("TourDate", back_populates="bookings")
    travelers = relationship(
        "Traveler", secondary=booking_travelers, back_populates="bookings"
    )
    payments = relationship("Payment", back_populates="booking")


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    payment_reference: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    amount: Mapped[float] = mapped_column(nullable=False)
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    payment_status: Mapped[str] = mapped_column(String(50), default="pending")
    trasaction_id: Mapped[str] = mapped_column(String(100), nullable=True)
    payment_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"), nullable=False)

    booking = relationship("Booking", back_populates="payments")


class Review(Base):
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str] = mapped_column(String(1000), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    tour_id: Mapped[int] = mapped_column(ForeignKey("tours.id"), nullable=False)

    user = relationship("Users", back_populates="reviews")
    tour = relationship("Tour", back_populates="reviews")
