from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache


from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException
from src.schemas.hotels import HotelPatch, HotelAdd
from src.services.hotels import HotelService

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
    hotels = await HotelService(db).get_filtered_by_time(
        pagination, location, title, date_from, date_to
    )

    return {"status": "OK", "data": hotels}


@router.get("/{hotel_id}")
@cache(expire=10)
async def get_hotel(
    hotel_id: int,
    db: DBDep,
):
    try:
        return await HotelService(db).get_hotel(hotel_id)
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
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def put_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelAdd,
):
    await HotelService(db).put_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Partial update of hotel data",
    description="<h1>You can change only the hotel data that you need</h1>",
)
async def patch_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPatch,
):
    await HotelService(db).patch_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(
    db: DBDep,
    hotel_id: int,
):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}
