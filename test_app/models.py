from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class Email(Base):
    """Represents an email record."""
    __tablename__ = 'emails'

    id = Column(String, primary_key=True, nullable=False)
    sender = Column(String, nullable=False)
    subject = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    received_datetime = Column(DateTime, nullable=False)
    labels = Column(Text, nullable=True)  # New column to store label IDs as a comma-separated string


DATABASE_URL = "sqlite:///emails.db"


def get_engine():
    """Create the SQLAlchemy engine."""
    return create_engine(DATABASE_URL)


def create_tables():
    """Create all tables defined in the models."""
    engine = get_engine()
    Base.metadata.create_all(engine)


Session = sessionmaker(bind=get_engine())
