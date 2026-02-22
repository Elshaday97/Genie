from app.core.config import config
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

# Standardized naming convention for all constraints
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


engine = create_engine(
    config.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,  # Ping database
    pool_size=10,  # Number of connections
    max_overflow=20,  # Allow 20 more during spikes
    pool_recycle=3600,  # Close connections older than 1 hour
)

SessionLocal = sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False, class_=Session
)


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)
