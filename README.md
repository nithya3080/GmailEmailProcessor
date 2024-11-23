```markdown
# GmailEmailProcessor

This project allows you to fetch and process emails from a Gmail account using the Gmail API. The script supports actions such as marking emails as read and moving them to specific labels based on user-defined rules. It uses SQLAlchemy to store email data in a local SQLite database.

## Features
- **Fetch Emails**: Retrieve emails from a Gmail account and store them in a local database.
- **Process Emails**: Apply rules to emails based on conditions such as sender, subject, and received time. Actions like marking as read and moving to labels are supported.
- **Dynamic Label Management**: Move emails to user-defined labels dynamically.
- **Error Handling**: Graceful error handling with logs for invalid labels or permissions.

## Requirements
- Python 3.x
- Gmail API enabled in Google Cloud Console
- Required Python libraries (listed below)

## Setup and Installation

### 1. Create Google Cloud Project and Enable Gmail API
Follow these steps to set up the Gmail API:

1. **Go to Google Cloud Console**.
2. **Create a new project** or select an existing one.
3. **Enable the Gmail API**:
   - Go to **APIs & Services > Library**.
   - Search for **Gmail API** and enable it.
4. **Create OAuth 2.0 credentials**:
   - Go to **APIs & Services > Credentials**.
   - Click **Create Credentials** and select **OAuth 2.0 Client IDs**.
   - Choose **Desktop App** for the application type.
   - Download the **credentials.json** file.

### 2. Install Python Dependencies
Clone the repository and install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

Here is the list of dependencies:
- `google-api-python-client`: For interacting with the Gmail API.
- `google-auth-httplib2`: For OAuth 2.0 authentication.
- `google-auth-oauthlib`: For OAuth 2.0 flow.
- `SQLAlchemy`: For database management.
- `sqlite3`: For using SQLite as the database (comes pre-installed with Python).

### 3. Set Up Google API Credentials
Place the **credentials.json** file you downloaded earlier into the project directory.

### 4. Database Setup
The database schema is automatically created when you run the application. SQLAlchemy will handle the creation of the emails table where email details will be stored.

### 5. Authentication and Authorization
When you run the script for the first time, it will authenticate using OAuth 2.0. A browser window will open, asking for permission to access your Gmail account. Once authenticated, a **token.json** file will be created to store the credentials for future use.

### 6. Create and Update Rules (`rules.json`)
Define rules for processing emails in the `rules.json` file. Here’s an example configuration:

```json
{
    "rules": [
        {
            "field": "From",
            "predicate": "contains",
            "value": "no-reply@accounts.google.com",
            "actions": ["mark_as_read"]
        },
        {
            "field": "Subject",
            "predicate": "equals",
            "value": "Some Handpicked Jobs for you!",
            "actions": ["move_to:Jobs"]
        }
    ]
}
```

#### Actions:
- `"mark_as_read"`: Marks the email as read by removing the UNREAD label.
- `"move_to:<LabelName>"`: Moves the email to a specified label (e.g., `"move_to:Jobs"`).

#### Fields and Predicates:
- **Fields**: From, Subject, etc.
- **Predicates**: contains, equals, less than, etc.

### 7. Run the Application

#### Fetch Emails:
Run the script to fetch emails from your Gmail account and store them in the SQLite database:

```bash
python fetch_emails.py
```

#### Process Emails:
Run the script to process the emails based on the rules defined in `rules.json`. This will mark emails as read or move them to labels:

```bash
python process_emails.py
```

## Error Handling

- **403: Insufficient Permissions**: If you receive a permission error, ensure that you have updated your `SCOPES` in `gmail_auth.py` to include `'https://www.googleapis.com/auth/gmail.modify'` for modifying emails.
- **Invalid Label**: Ensure that the label you're attempting to move the email to exists in Gmail. Use `get_label_mapping()` to fetch all available labels.

## Troubleshooting

- **OAuth Errors**: Delete **token.json** and re-authenticate by running the fetch or process script again.
- **Missing Labels**: Ensure that the labels you reference in `rules.json` are created in your Gmail account.
