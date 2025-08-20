from fastapi import APIRouter, Cookie, Depends, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from ...models.auth import Users
from ...schemas.auth_schemas import UserCreateSchema
from ...database.init_db import get_db
from ...utils.auth_helpers import (
    create_access_token,
    get_password_hash,
    verify_password,
    create_refresh_token,
    verify_refresh_token,
)

auth_router = APIRouter()


@auth_router.post("/signup")
async def signup(request: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Users).where(Users.email == request.email))
    exist_user = result.scalars().first()
    if exist_user:
        return JSONResponse(
            {"message": "User already exists"}, status_code=status.HTTP_400_BAD_REQUEST
        )

    result = await db.execute(select(Users).where(Users.phone == request.phone))
    exist_phone = result.scalars().first()
    if exist_phone:
        return JSONResponse(
            {"message": "Phone number already registered"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    result = await db.execute(select(func.count()).select_from(Users))
    user_count = result.scalar_one()
    role = "admin" if user_count == 0 else "user"

    new_user = Users(
        username=request.username,
        password=get_password_hash(request.password),
        email=request.email,
        role=role,
        first_name=request.first_name,
        last_name=request.last_name,
        phone=request.phone if request.phone else None,
    )
    db.add(new_user)
    await db.commit()
    return JSONResponse(
        {"message": "User created successfully"}, status_code=status.HTTP_201_CREATED
    )


@auth_router.post("/login")
async def login(
    response: Response,
    request: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Users).where(Users.email == request.username))
    user = result.scalars().first()
    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found"}
        )
    if not verify_password(request.password, user.password):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Invalid username or password"},
        )
    access_token = create_access_token(data={"sub": user.id, "role": user.role})
    refresh_token = create_refresh_token(data={"sub": user.id, "role": user.role})

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/refresh")
async def refresh(
    refresh_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db),
):
    if not refresh_token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Refresh token not found"},
        )

    try:
        payload = verify_refresh_token(refresh_token)
        user_id = payload.get("sub")

        if not user_id:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "Invalid refresh token"},
            )

        # Fetch user from DB
        result = await db.execute(select(Users).where(Users.id == int(user_id)))
        user = result.scalars().first()

        if not user:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "User not found"},
            )

        # Create new access token
        access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role}
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": f"Invalid or expired refresh token: {str(e)}"},
        )


@auth_router.post("/logout")
def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Logout successful"}
