from fastapi import APIRouter
from fastapi_cache.decorator import cache
from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import AllRoomsAreBookedException, AllRoomsAreBookedHTTPException
from src.schemas.bookings import BookingAddRequest
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("")
@cache(expire=10)
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get("/me")
@cache(expire=10)
async def get_my_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    return await BookingService(db).get_my_bookings(user_id)


@router.post("")
async def add_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingAddRequest,
):
    try:
        booking = await BookingService(db).add_booking(user_id, booking_data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException

    return {"status": "OK", "data": booking}
