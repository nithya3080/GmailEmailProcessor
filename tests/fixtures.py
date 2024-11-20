import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from test_app.models import Base

@pytest.fixture(scope='function')
def test_db():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
