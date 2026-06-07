from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import ObjectAlreadyExistsException
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication and authorisation"])


@router.post("/register")
async def register_user(
    db: DBDep,
    data: UserRequestAdd,
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, password=hashed_password)
    try:
        await db.users.add(new_user_data)
        await db.commit()
    except ObjectAlreadyExistsException:
        raise HTTPException(status_code=409, detail="A user with this email already exists")

    return {"status": "OK"}


@router.post("/login")
async def login_user(
    db: DBDep,
    data: UserRequestAdd,
    response: Response,
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="User with this email is not registered")
    if not AuthService().verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Wrong password")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(
    db: DBDep,
    user_id: UserIdDep,
):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout")
async def logout_user(responce: Response):
    responce.delete_cookie("access_token")
    return {"status": "OK"}
