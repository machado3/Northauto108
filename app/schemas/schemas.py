from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


# ── Photos ────────────────────────────────────────────────────────────────────


class PhotoOut(BaseModel):
  id: Optional[int] = None
  url: Optional[str] = None
  public_id: Optional[str] = None
  is_primary: Optional[bool] = None
  car_id: Optional[int] = None
  created_at: Optional[datetime] = None

  model_config = {"from_attributes": True}


# ── Cars ──────────────────────────────────────────────────────────────────────


class CarBase(BaseModel):
  title: Optional[str] = Field(default=None, min_length=1, max_length=255)
  brand: Optional[str] = Field(default=None, min_length=1, max_length=100)
  model: Optional[str] = Field(default=None, min_length=1, max_length=100)
  year: Optional[int] = Field(default=None, ge=1900, le=2100)
  price: Optional[Decimal] = Field(default=None, ge=0)
  mileage: Optional[int] = Field(default=None, ge=0)
  fuel: Optional[str] = Field(default=None, min_length=1, max_length=50)
  transmission: Optional[str] = Field(default=None, min_length=1, max_length=50)
  color: Optional[str] = Field(default=None, max_length=50)
  horsepower: Optional[int] = Field(default=None, ge=0)
  description: Optional[str] = Field(default=None)
  features: Optional[list[Optional[str]]] = Field(default=None)
  active: Optional[bool] = Field(default=None)


class CarCreate(CarBase):
  pass


class CarUpdate(BaseModel):
  title: Optional[str] = Field(default=None, min_length=1, max_length=255)
  brand: Optional[str] = Field(default=None, min_length=1, max_length=100)
  model: Optional[str] = Field(default=None, min_length=1, max_length=100)
  year: Optional[int] = Field(default=None, ge=1900, le=2100)
  price: Optional[Decimal] = Field(default=None, ge=0)
  mileage: Optional[int] = Field(default=None, ge=0)
  fuel: Optional[str] = Field(default=None, min_length=1, max_length=50)
  transmission: Optional[str] = Field(default=None, min_length=1, max_length=50)
  color: Optional[str] = Field(default=None, max_length=50)
  horsepower: Optional[int] = Field(default=None, ge=0)
  description: Optional[str] = None
  features: Optional[list[Optional[str]]] = None
  active: Optional[bool] = None


class CarOut(CarBase):
  id: Optional[int] = None
  photos: Optional[list[Optional[PhotoOut]]] = Field(default=None)
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None

  model_config = {"from_attributes": True}


class CarListOut(BaseModel):
  id: Optional[int] = None
  title: Optional[str] = None
  brand: Optional[str] = None
  model: Optional[str] = None
  year: Optional[int] = None
  price: Optional[Decimal] = None
  mileage: Optional[int] = None
  fuel: Optional[str] = None
  transmission: Optional[str] = None
  color: Optional[str] = None
  horsepower: Optional[int] = None
  features: Optional[list[Optional[str]]] = None
  active: Optional[bool] = None
  primary_photo: Optional[PhotoOut] = None
  photo_count: Optional[int] = 0
  created_at: Optional[datetime] = None

  model_config = {"from_attributes": True}


# ── Auth ──────────────────────────────────────────────────────────────────────


class LoginRequest(BaseModel):
  username: Optional[str] = None
  password: Optional[str] = None


class TokenResponse(BaseModel):
  access_token: Optional[str] = None
  token_type: Optional[str] = "bearer"
  username: Optional[str] = None


# ── Generic ───────────────────────────────────────────────────────────────────


class MessageResponse(BaseModel):
  message: Optional[str] = None