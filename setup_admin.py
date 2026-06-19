#!/usr/bin/env python3
"""
Script para criar o primeiro utilizador admin.
Corre com: python setup_admin.py
"""
import sys
import getpass

# Adicionar o diretório ao path
sys.path.insert(0, ".")

from app.core.database import engine, SessionLocal, Base
from app.models.models import Admin  # noqa
from app.core.auth import hash_password

Base.metadata.create_all(bind=engine)

def main():
    print("\n🚗 CarSite Backend — Setup do Admin\n")

    db = SessionLocal()

    existing = db.query(Admin).all()
    if existing:
        print(f"Já existe(m) {len(existing)} admin(s): {[a.username for a in existing]}")
        resp = input("Criar outro? (s/N): ").strip().lower()
        if resp != "s":
            db.close()
            return

    username = input("Username: ").strip()
    if not username:
        print("Username não pode estar vazio.")
        db.close()
        return

    if db.query(Admin).filter(Admin.username == username).first():
        print(f"Já existe um admin com o username '{username}'.")
        db.close()
        return

    password = getpass.getpass("Password: ")
    if len(password) < 6:
        print("A password deve ter pelo menos 6 caracteres.")
        db.close()
        return

    confirm = getpass.getpass("Confirmar password: ")
    if password != confirm:
        print("As passwords não coincidem.")
        db.close()
        return

    admin = Admin(username=username, password=hash_password(password))
    db.add(admin)
    db.commit()
    db.close()

    print(f"\n✅ Admin '{username}' criado com sucesso!")
    print("Arranca o servidor com: uvicorn app.main:app --reload")
    print("Docs: http://localhost:8000/docs\n")


if __name__ == "__main__":
    main()
