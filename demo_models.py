# from sqlalchemy import (
#     Column,
#     Integer,
#     String,
#     Text,
#     DateTime,
#     Boolean,
#     ForeignKey,
#     Decimal,
#     Table,
# )
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from datetime import datetime

# Base = declarative_base()

# # Association tables for many-to-many relationships
# tour_amenities = Table(
#     "tour_amenities",
#     Base.metadata,
#     Column("tour_id", Integer, ForeignKey("tours.id"), primary_key=True),
#     Column("amenity_id", Integer, ForeignKey("amenities.id"), primary_key=True),
# )

# tour_categories = Table(
#     "tour_categories",
#     Base.metadata,
#     Column("tour_id", Integer, ForeignKey("tours.id"), primary_key=True),
#     Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
# )

# booking_travelers = Table(
#     "booking_travelers",
#     Base.metadata,
#     Column("booking_id", Integer, ForeignKey("bookings.id"), primary_key=True),
#     Column("traveler_id", Integer, ForeignKey("travelers.id"), primary_key=True),
# )


# # Main Models
# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String(255), unique=True, index=True, nullable=False)
#     username = Column(String(100), unique=True, index=True, nullable=False)
#     hashed_password = Column(String(255), nullable=False)
#     first_name = Column(String(100), nullable=False)
#     last_name = Column(String(100), nullable=False)
#     phone = Column(String(20))
#     is_active = Column(Boolean, default=True)
#     is_verified = Column(Boolean, default=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     # Relationships
#     bookings = relationship("Booking", back_populates="user")
#     reviews = relationship("Review", back_populates="user")
#     travelers = relationship("Traveler", back_populates="user")


# class Destination(Base):
#     __tablename__ = "destinations"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(200), nullable=False, index=True)
#     country = Column(String(100), nullable=False)
#     state = Column(String(100))
#     city = Column(String(100))
#     description = Column(Text)
#     image_url = Column(String(500))
#     latitude = Column(Decimal(10, 8))
#     longitude = Column(Decimal(11, 8))
#     is_active = Column(Boolean, default=True)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     # Relationships
#     tours = relationship("Tour", back_populates="destination")


# class Category(Base):
#     __tablename__ = "categories"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), unique=True, nullable=False)
#     description = Column(Text)
#     icon = Column(String(100))  # For storing icon class names
#     is_active = Column(Boolean, default=True)

#     # Relationships
#     tours = relationship("Tour", secondary=tour_categories, back_populates="categories")


# class Amenity(Base):
#     __tablename__ = "amenities"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), unique=True, nullable=False)
#     description = Column(String(255))
#     icon = Column(String(100))

#     # Relationships
#     tours = relationship("Tour", secondary=tour_amenities, back_populates="amenities")


# class Tour(Base):
#     __tablename__ = "tours"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(200), nullable=False, index=True)
#     description = Column(Text, nullable=False)
#     short_description = Column(String(500))
#     duration_days = Column(Integer, nullable=False)
#     duration_nights = Column(Integer)
#     max_participants = Column(Integer, nullable=False)
#     min_participants = Column(Integer, default=1)
#     price_per_person = Column(Decimal(10, 2), nullable=False)
#     discount_percentage = Column(Decimal(5, 2), default=0)
#     image_url = Column(String(500))
#     is_active = Column(Boolean, default=True)
#     is_featured = Column(Boolean, default=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     # Foreign Keys
#     destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)

#     # Relationships
#     destination = relationship("Destination", back_populates="tours")
#     categories = relationship(
#         "Category", secondary=tour_categories, back_populates="tours"
#     )
#     amenities = relationship(
#         "Amenity", secondary=tour_amenities, back_populates="tours"
#     )
#     tour_dates = relationship("TourDate", back_populates="tour")
#     bookings = relationship("Booking", back_populates="tour")
#     reviews = relationship("Review", back_populates="tour")
#     itinerary_items = relationship("ItineraryItem", back_populates="tour")


# class TourDate(Base):
#     __tablename__ = "tour_dates"

#     id = Column(Integer, primary_key=True, index=True)
#     start_date = Column(DateTime, nullable=False)
#     end_date = Column(DateTime, nullable=False)
#     available_spots = Column(Integer, nullable=False)
#     price_per_person = Column(Decimal(10, 2))  # Can override tour price
#     is_active = Column(Boolean, default=True)

#     # Foreign Keys
#     tour_id = Column(Integer, ForeignKey("tours.id"), nullable=False)

#     # Relationships
#     tour = relationship("Tour", back_populates="tour_dates")
#     bookings = relationship("Booking", back_populates="tour_date")


# class ItineraryItem(Base):
#     __tablename__ = "itinerary_items"

#     id = Column(Integer, primary_key=True, index=True)
#     day_number = Column(Integer, nullable=False)
#     title = Column(String(200), nullable=False)
#     description = Column(Text)
#     activities = Column(Text)
#     meals_included = Column(String(100))  # breakfast, lunch, dinner
#     accommodation = Column(String(200))

#     # Foreign Keys
#     tour_id = Column(Integer, ForeignKey("tours.id"), nullable=False)

#     # Relationships
#     tour = relationship("Tour", back_populates="itinerary_items")


# class Traveler(Base):
#     __tablename__ = "travelers"

#     id = Column(Integer, primary_key=True, index=True)
#     first_name = Column(String(100), nullable=False)
#     last_name = Column(String(100), nullable=False)
#     email = Column(String(255))
#     phone = Column(String(20))
#     date_of_birth = Column(DateTime)
#     passport_number = Column(String(50))
#     nationality = Column(String(100))

#     # Foreign Keys
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

#     # Relationships
#     user = relationship("User", back_populates="travelers")
#     bookings = relationship(
#         "Booking", secondary=booking_travelers, back_populates="travelers"
#     )


# class Booking(Base):
#     __tablename__ = "bookings"

#     id = Column(Integer, primary_key=True, index=True)
#     booking_reference = Column(String(20), unique=True, nullable=False)
#     number_of_travelers = Column(Integer, nullable=False)
#     total_amount = Column(Decimal(10, 2), nullable=False)
#     payment_status = Column(
#         String(50), default="pending"
#     )  # pending, paid, cancelled, refunded
#     booking_status = Column(
#         String(50), default="confirmed"
#     )  # confirmed, cancelled, completed
#     special_requests = Column(Text)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     # Foreign Keys
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     tour_id = Column(Integer, ForeignKey("tours.id"), nullable=False)
#     tour_date_id = Column(Integer, ForeignKey("tour_dates.id"), nullable=False)

#     # Relationships
#     user = relationship("User", back_populates="bookings")
#     tour = relationship("Tour", back_populates="bookings")
#     tour_date = relationship("TourDate", back_populates="bookings")
#     travelers = relationship(
#         "Traveler", secondary=booking_travelers, back_populates="bookings"
#     )
#     payments = relationship("Payment", back_populates="booking")


# class Payment(Base):
#     __tablename__ = "payments"

#     id = Column(Integer, primary_key=True, index=True)
#     payment_reference = Column(String(100), unique=True, nullable=False)
#     amount = Column(Decimal(10, 2), nullable=False)
#     payment_method = Column(
#         String(50), nullable=False
#     )  # card, bank_transfer, paypal, etc.
#     payment_status = Column(
#         String(50), default="pending"
#     )  # pending, completed, failed, refunded
#     transaction_id = Column(String(255))  # External payment gateway transaction ID
#     payment_date = Column(DateTime)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     # Foreign Keys
#     booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)

#     # Relationships
#     booking = relationship("Booking", back_populates="payments")


# class Review(Base):
#     __tablename__ = "reviews"

#     id = Column(Integer, primary_key=True, index=True)
#     rating = Column(Integer, nullable=False)  # 1-5 stars
#     title = Column(String(200))
#     comment = Column(Text)
#     is_verified = Column(Boolean, default=False)  # Only users who booked can review
#     is_approved = Column(Boolean, default=True)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     # Foreign Keys
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     tour_id = Column(Integer, ForeignKey("tours.id"), nullable=False)

#     # Relationships
#     user = relationship("User", back_populates="reviews")
#     tour = relationship("Tour", back_populates="reviews")
