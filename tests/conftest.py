import os
import pytest
from dotenv import load_dotenv

load_dotenv()

test_url = os.getenv("DATABASE_URL_TEST")
if not test_url:
    raise RuntimeError("DATABASE_URL_TEST is missing. Check your .env")

## Set database url to test NOT prod
os.environ["DATABASE_URL"] = test_url

# Viktigt: rensa settings-cache så den läser nya env
from app.core.config import get_settings
get_settings.cache_clear()

# Nu är det säkert att importera app/engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.db.models import Base
from app.db.session import get_db

# Testengine
engine = create_engine(test_url, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Skapa om tabeller för test-sessionen
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db_session():
    # En transaktion per test → rollback efter testet
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture()
def client(db_session):
    # Override get_db så API:t använder test-sessionen
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()