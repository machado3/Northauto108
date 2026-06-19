from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ── Photos ────────────────────────────────────────────────────────────────────

class PhotoOut(BaseModel):
    id: int
    url: str
    filename: str
    is_primary: bool
    car_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Cars ──────────────────────────────────────────────────────────────────────

class CarBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    brand: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=1900, le=2100)
    price: float = Field(..., ge=0)
    mileage: int = Field(default=0, ge=0)
    fuel: str = Field(..., min_length=1, max_length=50)
    transmission: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="", max_length=50)
    horsepower: Optional[int] = Field(default=None, ge=0)
    description: str = Field(default="")
    features: list[str] = Field(default=[])
    active: bool = Field(default=True)


class CarCreate(CarBase):
    pass


class CarUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    brand: Optional[str] = Field(default=None, min_length=1, max_length=100)
    model: Optional[str] = Field(default=None, min_length=1, max_length=100)
    year: Optional[int] = Field(default=None, ge=1900, le=2100)
    price: Optional[float] = Field(default=None, ge=0)
    mileage: Optional[int] = Field(default=None, ge=0)
    fuel: Optional[str] = Field(default=None, min_length=1, max_length=50)
    transmission: Optional[str] = Field(default=None, min_length=1, max_length=50)
    color: Optional[str] = Field(default=None, max_length=50)
    horsepower: Optional[int] = Field(default=None, ge=0)
    description: Optional[str] = None
    features: Optional[list[str]] = None
    active: Optional[bool] = None


class CarOut(CarBase):
    id: int
    photos: list[PhotoOut] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CarListOut(BaseModel):
    id: int
    title: str
    brand: str
    model: str
    year: int
    price: float
    mileage: int
    fuel: str
    transmission: str
    color: str
    horsepower: Optional[int]
    features: list[str]
    active: bool
    primary_photo: Optional[PhotoOut] = None
    photo_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Auth ──────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str


# ── Generic ───────────────────────────────────────────────────────────────────

class MessageResponse(BaseModel):
    message: str
