from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base
from app.core import cloudinary  # noqa: F401
from app.models import models  # noqa: F401
from app.routers import cars, auth, admin_cars, admin_photos

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description="""
## CarSite API

Backend REST para site de anúncios de carros.

### Autenticação
Os endpoints de backoffice (`/admin/*`) requerem um **Bearer Token** JWT.

1. Faz `POST /admin/auth/login`
2. Usa `Authorization: Bearer <token>`

### Docs
- Swagger UI: `/docs`
- ReDoc: `/redoc`
""",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cars.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(admin_cars.router, prefix="/api/v1")
app.include_router(admin_photos.router, prefix="/api/v1")


@app.get("/", tags=["Root"])
def root():
    return {
        "app": settings.APP_TITLE,
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health", tags=["Root"])
def health():
    return {"status": "ok"}