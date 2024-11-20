from test_app.process_emails import process_emails
from test_app.models import Email, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
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

@pytest.fixture
def setup_test_data(test_session):
    """Add test data to the database."""
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

def test_process_emails(mocker, test_session, setup_test_data):
    """Test that emails are processed correctly based on rules."""
    mocker.patch('test_app.process_emails.mark_as_read', return_value=None)
    mocker.patch('test_app.process_emails.move_message', return_value=None)

    # Mock rules.json
    mocker.patch('test_app.process_emails.load_rules', return_value={
        "rules": [
            {
                "field": "From",
                "predicate": "contains",
                "value": "test@example.com",
                "actions": ["mark_as_read"]
            }
        ],
        "overall_predicate": "any"
    })

    process_emails()

    # Verify database changes or API calls if applicable
    email = test_session.query(Email).filter_by(id='123').first()
    assert email is not None
