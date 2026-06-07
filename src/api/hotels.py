from datetime import date
from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache


from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import (
    check_date_from_before_date_to,
    ObjectNotFoundException,
    HotelNotFoundHTTPException,
)
from src.schemas.hotels import HotelPatch, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Name of hotel"),
    location: str | None = Query(None, description="Address of hotel"),
    date_from: date = Query(example="2026-08-04"),
    date_to: date = Query(example="2026-08-15"),
):
    check_date_from_before_date_to(date_from, date_to)
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )


@router.get("/{hotel_id}")
@cache(expire=10)
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Prague",
                "value": {
                    "title": "Central Hotel 5*",
                    "location": "Opletalova 1, 11000 Prague, Czech Republic",
                },
            },
            "2": {
                "summary": "Brno",
                "value": {
                    "title": "Holiday Inn",
                    "location": "Smetanova 760/24, 60200 Brno, Czech Republic",
                },
            },
        }
    ),
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def put_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Partial update of hotel data",
    description="<h1>Here we partially update the hotel data: you can send the title, or the location</h1>",
)
async def patch_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}
