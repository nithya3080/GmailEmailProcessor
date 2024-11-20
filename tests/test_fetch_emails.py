import pytest
from test_app.fetch_emails import fetch_and_store_emails
from test_app.models import Email, Session

def test_fetch_emails(mocker):
    """Test that emails are fetched and stored correctly."""
    # Mock the Gmail API service
    mock_service = mocker.Mock()
    mock_messages = {
        'messages': [
            {'id': '123', 'snippet': 'Test email'},
        ]
    }
    mock_service.users().messages().list().execute.return_value = mock_messages
    mock_message_detail = {
        'id': '123',
        'snippet': 'Test email body',
        'payload': {'headers': [{'name': 'From', 'value': 'test@example.com'}, {'name': 'Subject', 'value': 'Test Subject'}]},
        'internalDate': '1699000000000',
        'labelIds': ['INBOX', 'UNREAD'],
    }
    mock_service.users().messages().get().execute.return_value = mock_message_detail

    # Mock Gmail authentication
    mocker.patch('test_app.fetch_emails.authenticate_gmail', return_value=mock_service)

    # Test fetch_and_store_emails
    session = Session()
    fetch_and_store_emails()

    # Check if the email was added to the database
    email = session.query(Email).filter_by(id='123').first()
    assert email is not None
    assert email.sender == 'test@example.com'
    assert email.subject == 'Test Subject'
    assert 'INBOX' in email.labels
