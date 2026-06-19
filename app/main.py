from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings
from app.core.database import engine, Base
from app.models import models  # noqa: F401 — registar modelos no SQLAlchemy
from app.routers import cars, auth, admin_cars, admin_photos

# Criar tabelas na base de dados
Base.metadata.create_all(bind=engine)

# Garantir pasta de uploads
os.makedirs(os.path.join(settings.UPLOAD_DIR, "cars"), exist_ok=True)

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description="""
## CarSite API

Backend REST para site de anúncios de carros.

### Autenticação
Os endpoints de backoffice (`/admin/*`) requerem um **Bearer Token** JWT.

1. Faz `POST /admin/auth/login` com `{ username, password }`
2. Usa o `access_token` no header: `Authorization: Bearer <token>`

### Docs interativas
- Swagger UI: `/docs`
- ReDoc: `/redoc`
    """,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — permite o frontend Next.js ligar ao backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir ficheiros de upload estaticamente
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Routers
app.include_router(cars.router,          prefix="/api/v1")
app.include_router(auth.router,          prefix="/api/v1")
app.include_router(admin_cars.router,    prefix="/api/v1")
app.include_router(admin_photos.router,  prefix="/api/v1")


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
