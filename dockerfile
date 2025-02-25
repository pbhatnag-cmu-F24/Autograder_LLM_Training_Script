# Start from a Python base image
FROM python:3.9-slim

# Create a working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Specify the command to run your app
CMD ["python", "app.py"]
