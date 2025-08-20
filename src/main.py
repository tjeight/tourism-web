from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .database.init_db import create_tables
from contextlib import asynccontextmanager
from .api.v1.auth_routes import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])


@app.get("/")
def read_root():
    return JSONResponse({"message": "This is the home page"})
