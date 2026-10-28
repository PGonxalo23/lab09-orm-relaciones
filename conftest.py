# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from modelos import Base
 
 
@pytest.fixture(scope="function")
def db_session():
    """Fixture que provee una sesion limpia de SQLite en memoria para cada test."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
 
    yield session
 
    session.close()
    engine.dispose()
