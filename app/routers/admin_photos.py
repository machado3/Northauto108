import uuid
import cloudinary.uploader
from app.core import cloudinary
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_admin
from app.core.config import settings
from app.models.models import Car, Photo, Admin
from app.schemas.schemas import PhotoOut, MessageResponse

router = APIRouter(prefix="/admin/cars/{car_id}/photos", tags=["Backoffice - Fotos"])

ALLOWED_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
MAX_SIZE = settings.MAX_FILE_SIZE_MB * 1024 * 1024


def get_car_or_404(car_id: int, db: Session) -> Car:
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Carro não encontrado")
    return car


@router.get("", response_model=list[PhotoOut], summary="Listar fotos de um carro")
def list_photos(
    car_id: int,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    car = get_car_or_404(car_id, db)
    return car.photos


@router.post("", response_model=PhotoOut, status_code=201, summary="Fazer upload de uma foto")
async def upload_photo(
    car_id: int,
    file: UploadFile = File(..., description="Imagem JPG, PNG ou WebP (máx. 10MB)"),
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    car = get_car_or_404(car_id, db)

    # Validar tipo
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo inválido: {file.content_type}. Usa JPG, PNG ou WebP.",
        )

    # Ler conteúdo e validar tamanho
    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Ficheiro demasiado grande. Máximo {settings.MAX_FILE_SIZE_MB}MB.",
        )

    # Gerar nome único
    result = cloudinary.uploader.upload(
    content,
    folder=f"cars/{car_id}",
    public_id=uuid.uuid4().hex,
    overwrite=False,
    resource_type="image",
)

    url = result["secure_url"]
    public_id = result["public_id"]

    # Primeira foto é sempre a principal
    is_primary = len(car.photos) == 0

    photo = Photo(url=url, public_id=public_id, is_primary=is_primary, car_id=car_id)
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo


@router.delete("/{photo_id}", response_model=MessageResponse, summary="Apagar uma foto")
def delete_photo(
    car_id: int,
    photo_id: int,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    photo = db.query(Photo).filter(Photo.id == photo_id, Photo.car_id == car_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Foto não encontrada")

    was_primary = photo.is_primary

    # Apagar ficheiro físico
    cloudinary.uploader.destroy(photo.public_id)

    db.delete(photo)
    db.commit()

    # Se era a principal, promover a próxima
    if was_primary:
        car = db.query(Car).filter(Car.id == car_id).first()
        if car and car.photos:
            car.photos[0].is_primary = True
            db.commit()

    return {"message": f"Foto #{photo_id} apagada"}


@router.patch("/{photo_id}/primary", response_model=PhotoOut, summary="Definir foto principal")
def set_primary_photo(
    car_id: int,
    photo_id: int,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    photo = db.query(Photo).filter(Photo.id == photo_id, Photo.car_id == car_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Foto não encontrada")

    # Remover principal atual
    db.query(Photo).filter(Photo.car_id == car_id, Photo.is_primary == True).update(
        {"is_primary": False}
    )
    photo.is_primary = True
    db.commit()
    db.refresh(photo)
    return photo
