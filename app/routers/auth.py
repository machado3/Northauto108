from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import hash_password, verify_password, create_access_token, get_current_admin
from app.models.models import Admin
from app.schemas.schemas import LoginRequest, TokenResponse, MessageResponse

router = APIRouter(prefix="/admin/auth", tags=["Backoffice - Auth"])


@router.post("/login", response_model=TokenResponse, summary="Login do admin")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == data.username).first()
    if not admin or not verify_password(data.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username ou password incorretos",
        )
    token = create_access_token({"sub": admin.username, "id": admin.id})
    return TokenResponse(access_token=token, username=admin.username)


@router.get("/me", summary="Dados do admin autenticado")
def me(admin: Admin = Depends(get_current_admin)):
    return {"id": admin.id, "username": admin.username}
