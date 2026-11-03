from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.config import settings

class Base(DeclarativeBase): pass
_is_sqlite = settings.database_url.startswith("sqlite")
_connect_args = {"check_same_thread": False} if _is_sqlite else {}
_pool = {"poolclass": StaticPool} if settings.database_url in ("sqlite://", "sqlite:///:memory:") else {}
engine = create_engine(settings.database_url, connect_args=_connect_args, pool_pre_ping=True, **_pool)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
