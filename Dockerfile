# Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy necessary folders
COPY app/ app/
COPY input/ input/
COPY output/ output/

# Install dependencies
RUN pip install --no-cache-dir -r app/requirements.txt

# Set default command
CMD ["python", "app/main.py"]
