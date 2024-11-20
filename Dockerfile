# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose optional ports for debugging
EXPOSE 8000

# Default command to run fetch_emails.py
CMD ["python", "test_app/fetch_emails.py"]
