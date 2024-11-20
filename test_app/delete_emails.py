from models import Session, Email

def delete_all_emails():
    """Delete all entries from the Email table."""
    session = Session()
    try:
        # Delete all rows in the Email table
        session.query(Email).delete()
        session.commit()
        print("All entries in the Email table have been deleted.")
    except Exception as e:
        session.rollback()
        print(f"Error deleting entries: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    delete_all_emails()
