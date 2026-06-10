from datetime import date
from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache
from src.api.dependencies import DBDep
from src.exceptions import (
    HotelNotFoundHTTPException,
    RoomNotFoundHTTPException,
    HotelNotFoundException,
    RoomNotFoundException,
)
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
@cache(expire=10)
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2026-08-04"),
    date_to: date = Query(example="2026-08-15"),
):
    return await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
@cache(expire=10)
async def get_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    try:
        return await RoomService(db).get_room(room_id, hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms")
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body()):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest,
):
    await RoomService(db).edit_room(hotel_id, room_id, room_data)

    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Partial update of room data",
    description="<h1>You can change only the room data that you need</h1>",
)
async def patch_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
):
    await RoomService(db).patch_room(hotel_id, room_id, room_data)

    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    await RoomService(db).delete_room(hotel_id, room_id)

    return {"status": "OK"}
