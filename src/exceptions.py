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


class IncorrectTokenException(BookedException):
    detail = "Invalid token"


class ObjectAlreadyExistsException(BookedException):
    detail = "A similar object already exists"


class EmailNotRegisteredException(BookedException):
    detail = "No user with this email address is registered"


class IncorrectPasswordException(BookedException):
    detail = "Incorrect password"


class UserAlreadyExistsException(BookedException):
    detail = "The user already exists"


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


class AllRoomsAreBookedHTTPException(BookedHTTPException):
    status_code = 409
    detail = "There are no rooms available"


class IncorrectTokenHTTPException(BookedHTTPException):
    detail = "Invalid token"


class EmailNotRegisteredHTTPException(BookedHTTPException):
    status_code = 401
    detail = "No user with this email address is registered"


class UserEmailAlreadyExistsHTTPException(BookedHTTPException):
    status_code = 409
    detail = "A user with that email address already exists"


class IncorrectPasswordHTTPException(BookedHTTPException):
    status_code = 401
    detail = "Incorrect password"


class NoAccessTokenHTTPException(BookedHTTPException):
    status_code = 401
    detail = "You have not provided an access token"


class StaticHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class PageNotFoundHTTPException(StaticHTTPException):
    status_code = 404
    detail = "Page not found"
