from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings


class Base(DeclarativeBase):
    pass


database_url = make_url(settings.database_url)

_is_sqlite = database_url.get_backend_name() == "sqlite"

_connect_args = {}
_pool_args = {}

if _is_sqlite:
    _connect_args = {"check_same_thread": False}

    # Ensure the SQLite database directory exists
    if database_url.database not in (None, "", ":memory:"):
        db_path = Path(database_url.database).expanduser().resolve()
        db_path.parent.mkdir(parents=True, exist_ok=True)
        database_url = database_url.set(database=str(db_path))

    # Use StaticPool for an in-memory database
    if database_url.database in (None, "", ":memory:"):
        _pool_args = {"poolclass": StaticPool}

engine = create_engine(
    database_url,
    connect_args=_connect_args,
    pool_pre_ping=True,
    **_pool_args,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
