# Use a Python base image
FROM python:3.10-slim

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    libimage-exiftool-perl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install py3exiv2

# Set up working directory
WORKDIR /app

# Copy the Python script into the container
COPY scan_exif.py /app/

# Set the directory to scan as a default environment variable
ENV SCAN_DIR /data

# Command to run the script
CMD ["python", "scan_exif.py"]
