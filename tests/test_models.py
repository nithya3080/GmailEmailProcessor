from test_app.models import Email, Session, create_tables, Base
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

@pytest.fixture(scope='function')
def test_session():
    """Set up a temporary SQLite database for testing."""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)  # Create tables
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_email_model(test_session):
    """Test the Email model."""
    # Add a test email with a unique ID
    email = Email(
        id='123',
        sender='test@example.com',
        subject='Test Subject',
        message='This is a test email',
        received_datetime=datetime(2024, 11, 20, 10, 0, 0),  # Proper datetime object
        labels='INBOX,UNREAD'
    )
    test_session.add(email)
    test_session.commit()

    # Retrieve the email
    retrieved_email = test_session.query(Email).filter_by(id='123').first()
    assert retrieved_email.sender == 'test@example.com'
    assert retrieved_email.subject == 'Test Subject'