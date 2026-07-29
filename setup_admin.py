from app.core.database import engine, SessionLocal, Base
from app.models.models import Admin, Car, Photo  # Importa todos os teus modelos para o SQLAlchemy os registar
from app.core.auth import hash_password

def init_database():
    print("A criar tabelas na base de dados do Supabase...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas verificadas/criadas com sucesso!")

def create_admin():
    # Inicializa as tabelas primeiro
    init_database()

    db = SessionLocal()
    try:
        username = input("Insere o username do admin: ").strip()
        password = input("Insere a password do admin: ").strip()

        if not username or not password:
            print("Erro: O username e a password não podem estar vazios.")
            return

        # Verificar se o admin já existe
        existing = db.query(Admin).filter(Admin.username == username).first()
        if existing:
            print(f"O admin '{username}' já existe na base de dados.")
            return

        # Criar o novo admin
        hashed_pwd = hash_password(password)
        new_admin = Admin(username=username, password=hashed_pwd)
        
        db.add(new_admin)
        db.commit()
        print(f"Administrador '{username}' criado com sucesso no Supabase!")

    except Exception as e:
        db.rollback()
        print(f"Ocorreu um erro ao criar o admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()