# Use the official lightweight Python 3.13-3-slim-bookworm image
FROM python:3.13.3-slim-bookworm

# Set environment variables for Python optimization:
# - PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files
# - PYTHONUNBUFFERED: Ensures Python output is sent straight to terminal
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Update package lists and install minimal required system packages:
# - curl: For making HTTP requests (often needed for health checks)
# - ca-certificates: For SSL certificate verification
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Copy the uv (ultra-fast Python package installer) binary from Astral's official image
# This is more efficient than installing via pip
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy just the requirements file first (Docker caching optimization)
# This allows reusing cached layers if requirements don't change
COPY requirements.txt /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Python dependencies using uv instead of pip:
# - --system flag installs packages directly to system Python (no virtualenv)
RUN uv pip install -r requirements.txt --system

# Copy the rest of the application code into the container
# This comes after requirements to leverage Docker layer caching
COPY . /app

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python3", "-u", "main.py"]


