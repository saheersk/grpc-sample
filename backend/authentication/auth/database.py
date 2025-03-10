from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://task_auth_user:task_auth_user123@postgres_auth:5432/task_auth_db"
# SQLALCHEMY_DATABASE_URL = "postgresql://task_auth_user:task_auth_user123@postgres-fast-service:5432/task_auth_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
