from pydantic import BaseModel


class DestinationCreateSchema(BaseModel):
    name: str
    country: str
    description: str
    image_url: str


class DestinationOutputSchema(BaseModel):
    id: int
    name: str
    country: str
    description: str
    image_url: str


class DestinationUpdateSchema(BaseModel):
    name: str
    country: str
    description: str
    image_url: str


class CategoryCreateSchema(BaseModel):
    name: str
    description: str


class CategoryOutputSchema(BaseModel):
    id: int
    name: str
    description: str


class CategoryUpdateSchema(BaseModel):
    name: str
    description: str


class AmenityCreateSchema(BaseModel):
    name: str
    description: str


class AmenityOutputSchema(BaseModel):
    id: int
    name: str
    description: str


class AmenityUpdateSchema(BaseModel):
    name: str
    description: str


class TourCreateSchema(BaseModel):
    title: str
    description: str
    short_description: str
    duration_days: int
    duration_nights: int
    max_participants: int
    min_participants: int
    price_per_person: float
    discount_percentage: float
    image_url: str
    destination_id: int


class TourOutputSchema(BaseModel):
    id: int
    title: str
    description: str
    short_description: str
    duration_days: int
    duration_nights: int
    max_participants: int
    min_participants: int
    price_per_person: float
    discount_percentage: float
    image_url: str
    destination_id: int


class TourUpdateSchema(BaseModel):
    title: str
    description: str
    short_description: str
    duration_days: int
    duration_nights: int
    max_participants: int
    min_participants: int
    price_per_person: float
    discount_percentage: float
    image_url: str
    destination_id: int


class TourDateCreateSchema(BaseModel):
    start_date: str
    end_date: str
    tour_id: int
    available_slots: int
    price_per_person: float


class TourDateOutputSchema(BaseModel):
    id: int
    start_date: str
    end_date: str
    tour_id: int
    available_slots: int
    price_per_person: float


class TourDateUpdateSchema(BaseModel):
    start_date: str
    end_date: str
    available_slots: int
    price_per_person: float


class IntineraryCreateSchema(BaseModel):
    day_number: int
    title: str
    description: str
    activities: str
    meals_included: str
    accommodation: str
    tour_id: int


class IntineraryOutputSchema(BaseModel):
    id: int
    day_number: int
    title: str
    description: str
    activities: str
    meals_included: str
    accommodation: str
    tour_id: int


class IntineraryUpdateSchema(BaseModel):
    day_number: int
    title: str
    description: str
    activities: str
    meals_included: str
    accommodation: str


class TravelerCreateSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    user_id: int


class TravelerOutputSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    user_id: int


class TravelerUpdateSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str


class BookingCreateSchema(BaseModel):
    number_of_travelers: int
    total_amount: float
    payment_status: str
    booking_status: str
    special_requests: str
    user_id: int
    tour_id: int
    tour_date_id: int


class BookingOutputSchema(BaseModel):
    id: int
    number_of_travelers: int
    total_amount: float
    payment_status: str
    booking_status: str
    special_requests: str
    user_id: int
    tour_id: int
    tour_date_id: int


class BookingUpdateSchema(BaseModel):
    number_of_travelers: int
    total_amount: float
    payment_status: str
    booking_status: str
    special_requests: str
    user_id: int
    tour_id: int
    tour_date_id: int


class PaymentCreateSchema(BaseModel):
    amount: float
    payment_method: str
    payment_status: str
    transaction_id: str
    booking_id: int


class PaymentOutputSchema(BaseModel):
    id: int
    amount: float
    payment_method: str
    payment_status: str
    transaction_id: str
    booking_id: int


class PaymentUpdateSchema(BaseModel):
    amount: float
    payment_method: str
    payment_status: str
    transaction_id: str
    booking_id: int


class ReviewCreateSchema(BaseModel):
    rating: int
    comment: str
    user_id: int
    tour_id: int


class ReviewOutputSchema(BaseModel):
    id: int
    rating: int
    comment: str
    user_id: int
    tour_id: int


class ReviewUpdateSchema(BaseModel):
    rating: int
    comment: str
    user_id: int
    tour_id: int
