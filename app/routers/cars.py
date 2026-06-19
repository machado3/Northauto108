import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Car, Photo
from app.schemas.schemas import CarOut, CarListOut, PhotoOut

router = APIRouter(prefix="/cars", tags=["Carros (público)"])


def car_to_list_out(car: Car) -> CarListOut:
    primary = next((p for p in car.photos if p.is_primary), None) or (car.photos[0] if car.photos else None)
    return CarListOut(
        id=car.id,
        title=car.title,
        brand=car.brand,
        model=car.model,
        year=car.year,
        price=car.price,
        mileage=car.mileage,
        fuel=car.fuel,
        transmission=car.transmission,
        color=car.color,
        horsepower=car.horsepower,
        features=json.loads(car.features) if car.features else [],
        active=car.active,
        primary_photo=PhotoOut.model_validate(primary) if primary else None,
        photo_count=len(car.photos),
        created_at=car.created_at,
    )


@router.get("", response_model=list[CarListOut], summary="Listar carros ativos")
def list_cars(
    brand: Optional[str] = Query(None, description="Filtrar por marca"),
    fuel: Optional[str] = Query(None, description="Filtrar por combustível"),
    transmission: Optional[str] = Query(None, description="Filtrar por transmissão"),
    min_price: Optional[float] = Query(None, ge=0, description="Preço mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Preço máximo"),
    min_year: Optional[int] = Query(None, description="Ano mínimo"),
    max_year: Optional[int] = Query(None, description="Ano máximo"),
    max_mileage: Optional[int] = Query(None, ge=0, description="Quilómetros máximos"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    q = db.query(Car).filter(Car.active == True)

    if brand:
        q = q.filter(Car.brand.ilike(f"%{brand}%"))
    if fuel:
        q = q.filter(Car.fuel == fuel)
    if transmission:
        q = q.filter(Car.transmission == transmission)
    if min_price is not None:
        q = q.filter(Car.price >= min_price)
    if max_price is not None:
        q = q.filter(Car.price <= max_price)
    if min_year is not None:
        q = q.filter(Car.year >= min_year)
    if max_year is not None:
        q = q.filter(Car.year <= max_year)
    if max_mileage is not None:
        q = q.filter(Car.mileage <= max_mileage)

    cars = q.order_by(Car.created_at.desc()).offset(skip).limit(limit).all()
    return [car_to_list_out(c) for c in cars]


@router.get("/{car_id}", response_model=CarOut, summary="Detalhe de um carro")
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id, Car.active == True).first()
    if not car:
        raise HTTPException(status_code=404, detail="Carro não encontrado")

    # Deserializar features
    car_out = CarOut.model_validate(car)
    car_out.features = json.loads(car.features) if car.features else []
    return car_out
