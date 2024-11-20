from test_app.models import Email, create_tables, Session
from datetime import datetime
from test_app.utils.gmail_auth import authenticate_gmail


def fetch_and_store_emails():
    """Fetch emails using Gmail API and store them in the database."""
    service = authenticate_gmail()  # Authenticate with Gmail API
    create_tables()  # Ensure tables are created

    session = Session()

    # Fetch Gmail messages
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])

    for msg in messages:
        # Get detailed email data
        msg_detail = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = msg_detail['payload']['headers']
        sender = next((header['value'] for header in headers if header['name'] == 'From'), 'Unknown')
        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
        message_body = msg_detail['snippet']
        received_datetime = datetime.fromtimestamp(int(msg_detail['internalDate']) / 1000)

        # Fetch label IDs and join them into a comma-separated string
        label_ids = msg_detail.get('labelIds', [])
        label_ids_str = ','.join(label_ids)

        # Create or update email record
        email = Email(
            id=msg['id'],
            sender=sender,
            subject=subject,
            message=message_body,
            received_datetime=received_datetime,
            labels=label_ids_str  # Store label IDs
        )
        session.merge(email)  # Upsert operation
    session.commit()
    session.close()


if __name__ == '__main__':
    fetch_and_store_emails()
