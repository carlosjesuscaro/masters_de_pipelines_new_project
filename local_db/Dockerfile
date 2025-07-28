# Dockerfile for the Python data populator
FROM python:3.9-slim

WORKDIR /app

# Copy requirements.txt and install dependencies
# This creates a separate layer, so if requirements.txt doesn't change,
# this layer is cached and building is faster.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your data creation script
COPY data_creation.py .

# Command to run the script when the container starts
# This command will ONLY run your script, as dependencies are already installed.
CMD ["python", "data_creation.py"]