from test_app.models import Session, Email
from sqlalchemy import or_, and_
from test_app.utils.gmail_auth import authenticate_gmail
import json


def load_rules():
    """Load rules from a JSON file."""
    with open('test_app/rules.json', 'r') as file:
        return json.load(file)


def build_query(session, field, predicate, value, overall_predicate):
    field_mapping = {
        'From': Email.sender,
        'Subject': Email.subject,
        'Message': Email.message,
        'Received Date/Time': Email.received_datetime
    }
    if field not in field_mapping:
        raise ValueError(f"Invalid field: {field}")

    column = field_mapping[field]

    # Map predicates
    if predicate == 'contains':
        condition = column.like(f"%{value}%")
    elif predicate == 'equals':
        condition = column == value
    elif predicate == 'less than' and field == 'Received Date/Time':
        condition = column < value
    elif predicate == 'greater than' and field == 'Received Date/Time':
        condition = column > value
    else:
        raise ValueError(f"Invalid predicate: {predicate}")

    # Combine conditions based on overall_predicate
    if overall_predicate == "all":
        query = session.query(Email).filter(and_(condition))
    elif overall_predicate == "any":
        query = session.query(Email).filter(or_(condition))
    else:
        raise ValueError(f"Invalid overall predicate: {overall_predicate}")

    return query


def perform_actions(email, actions):
    """
    Perform actions on the matched emails dynamically resolving label IDs.

    Args:
        email: The email object (SQLAlchemy Email instance).
        actions: List of actions to perform (e.g., ['mark_as_read', 'move_to:INBOX']).
    """
    service = authenticate_gmail()  # Authenticate with Gmail API
    label_map = get_label_mapping(service)  # Fetch dynamic label mapping

    for action in actions:
        if action == 'mark_as_read':
            mark_as_read(service, email.id)
        elif action.startswith('move_to:'):
            # Extract label name and resolve its ID dynamically
            if ':' in action:
                label_name = action.split(':', 1)[1]
                label_id = label_map.get(label_name)
                if not label_id:
                    print(f"Error: Label '{label_name}' not found.")
                else:
                    move_message(service, email.id, label_id)
            else:
                print(f"Invalid 'move_to' action format: {action}")


def mark_as_read(service, email_id):
    """
    Mark an email as read using Gmail API.

    Args:
        service: Authenticated Gmail API service instance.
        email_id: The ID of the email to mark as read.
    """
    try:
        service.users().messages().modify(
            userId='me',
            id=email_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
        print(f"Email with ID {email_id} marked as read.")
    except Exception as e:
        print(f"Error marking email {email_id} as read: {e}")


def move_message(service, email_id, label_id):
    """
    Move an email to a specific label using Gmail API.

    Args:
        service: Authenticated Gmail API service instance.
        email_id: The ID of the email to move.
        label_id: The ID of the label to move the email to.
    """
    try:
        service.users().messages().modify(
            userId='me',
            id=email_id,
            body={'addLabelIds': [label_id], 'removeLabelIds': []}
        ).execute()
        print(f"Email with ID {email_id} moved to label ID {label_id}.")
    except Exception as e:
        print(f"Error moving email {email_id} to label ID {label_id}: {e}")


def get_label_mapping(service):
    """
    Fetch Gmail labels and create a mapping of label names to their IDs.

    Args:
        service: Authenticated Gmail API service instance.

    Returns:
        dict: A dictionary mapping label names to label IDs.
    """
    try:
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        label_map = {label['name']: label['id'] for label in labels}
        return label_map
    except Exception as e:
        print(f"Error fetching labels: {e}")
        return {}


def process_emails():
    """Process emails based on rules."""
    session = Session()
    rules = load_rules()  # Load the rules from the JSON file

    for rule in rules['rules']:
        field = rule['field']
        predicate = rule['predicate']
        value = rule['value']
        actions = rule['actions']

        # Build the SQLAlchemy query
        query = build_query(session, field, predicate, value, rules.get("overall_predicate", "any"))
        matched_emails = query.all()

        # Perform actions on matched emails
        for email in matched_emails:
            perform_actions(email, actions)

    session.close()


if __name__ == '__main__':
    process_emails()
