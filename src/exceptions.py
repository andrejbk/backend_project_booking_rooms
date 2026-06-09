from datetime import date

from fastapi import HTTPException


class BookedException(Exception):
    detail = "Unexpected error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BookedException):
    detail = "Object not found"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Room not found"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Hotel not found"


class AllRoomsAreBookedException(BookedException):
    detail = "There are no free rooms left"


class ObjectAlreadyExistsException(BookedException):
    detail = "A similar object already exists"


def check_date_from_before_date_to(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise HTTPException(
            status_code=422,
            detail="The check-in date cannot be later than or equal to the check-out date",
        )


class BookedHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(BookedHTTPException):
    status_code = 404
    detail = "Hotel not found"


class RoomNotFoundHTTPException(BookedHTTPException):
    status_code = 404
    detail = "Room not found"
