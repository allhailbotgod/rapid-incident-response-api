from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings

Base = declarative_base()
engine = create_engine(settings.DATABASE_URL)
local_session = sessionmaker(bind=engine, autoflush=False)


def get_db():
    db = local_session

    try:
        yield db
    finally:
        db.close()
