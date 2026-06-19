import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_admin
from app.models.models import Car, Admin
from app.schemas.schemas import CarCreate, CarUpdate, CarOut, CarListOut, MessageResponse
from app.routers.cars import car_to_list_out

router = APIRouter(prefix="/admin/cars", tags=["Backoffice - Anúncios"])


@router.get("", response_model=list[CarListOut], summary="Listar todos os anúncios")
def list_all_cars(
    active: Optional[bool] = Query(None, description="Filtrar por estado"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    q = db.query(Car)
    if active is not None:
        q = q.filter(Car.active == active)
    cars = q.order_by(Car.created_at.desc()).offset(skip).limit(limit).all()
    return [car_to_list_out(c) for c in cars]


@router.post("", response_model=CarOut, status_code=201, summary="Criar anúncio")
def create_car(
    data: CarCreate,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    car = Car(
        title=data.title,
        brand=data.brand,
        model=data.model,
        year=data.year,
        price=data.price,
        mileage=data.mileage,
        fuel=data.fuel,
        transmission=data.transmission,
        color=data.color,
        horsepower=data.horsepower,
        description=data.description,
        features=json.dumps(data.features, ensure_ascii=False),
        active=data.active,
    )
    db.add(car)
    db.commit()
    db.refresh(car)

    out = CarOut.model_validate(car)
    out.features = data.features
    return out


@router.get("/{car_id}", response_model=CarOut, summary="Detalhe de um anúncio")
def get_car(
    car_id: int,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado")
    out = CarOut.model_validate(car)
    out.features = json.loads(car.features) if car.features else []
    return out


@router.put("/{car_id}", response_model=CarOut, summary="Atualizar anúncio")
def update_car(
    car_id: int,
    data: CarUpdate,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado")

    update_data = data.model_dump(exclude_unset=True)
    if "features" in update_data:
        update_data["features"] = json.dumps(update_data["features"], ensure_ascii=False)

    for field, value in update_data.items():
        setattr(car, field, value)

    db.commit()
    db.refresh(car)

    out = CarOut.model_validate(car)
    out.features = json.loads(car.features) if car.features else []
    return out


@router.delete("/{car_id}", response_model=MessageResponse, summary="Apagar anúncio")
def delete_car(
    car_id: int,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado")

    # Apagar ficheiros físicos das fotos
    import os
    for photo in car.photos:
        path = f"uploads/cars/{photo.filename}"
        if os.path.exists(path):
            os.remove(path)

    db.delete(car)
    db.commit()
    return {"message": f"Anúncio #{car_id} apagado com sucesso"}
