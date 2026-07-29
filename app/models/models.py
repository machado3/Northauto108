from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects.postgresql import JSONB


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    mileage = Column(Integer, default=0)
    fuel = Column(String(50), nullable=False)
    transmission = Column(String(50), nullable=False)
    color = Column(String(50), default="")
    horsepower = Column(Integer, nullable=True)
    description = Column(Text, default="")
    features = Column(MutableList.as_mutable(JSONB), default=list)  # JSON array guardado como string
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    photos = relationship("Photo", back_populates="car", cascade="all, delete-orphan", order_by="Photo.is_primary.desc()", lazy="selectin")


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(Text, nullable=False)
    public_id = Column(String(500), nullable=False)
    is_primary = Column(Boolean, default=False)
    car_id = Column(Integer,ForeignKey("cars.id", ondelete="CASCADE"),nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    car = relationship("Car", back_populates="photos")

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
