# Container for i-want-to-track-and-analyze-my-life
# Base image
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY src/ /app/src/
COPY README.md /app/

# Ensure output directory exists (will be bind-mounted in compose typically)
RUN mkdir -p /app/DataBase

# Default command: fetch and export data
CMD ["python", "src/process_data.py"]

