"""Create initial LanguageHub schema."""
from alembic import op
from app.db import Base
from app import models  # noqa: F401 - register all model tables

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    Base.metadata.create_all(bind=op.get_bind())

def downgrade():
    # Drop only tables owned by this application's SQLAlchemy metadata.
    for table in reversed(Base.metadata.sorted_tables):
        op.drop_table(table.name)
