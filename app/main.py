from fastapi import FastAPI
from fastapi.responses  import JSONResponse
from .routes import routes
from app.config.db import create_db_and_tables
from app.config.config import settings
from contextlib import asynccontextmanager
# import redis

# redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True, username=settings.REDIS_USER, password=settings.REDIS_PASSWORD)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    # Here you can add any cleanup code if needed
    
app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# @app.middleware("http")
# async def rate_limit_middleware(request, call_next):
#     ip_address = request.client.host
#     rate_limit_key = f"rate_limit:{ip_address}"
#     try:
#         current_requests = redis_client.get(rate_limit_key)

#         if current_requests is None:
#             redis_client.set(rate_limit_key, 1, ex=settings.RATE_LIMIT_WINDOW)
#         elif int(current_requests) < settings.RATE_LIMIT_MAX_REQUESTS:
#             redis_client.incr(rate_limit_key)
#         else:
#             return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
#         response = await call_next(request)
#         return response
#     except redis.RedisError as e:
#         return JSONResponse(status_code=500, content={"detail": "Redis error occurred", "error": str(e)})

app.include_router(routes.router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the URL Shortener API!"}