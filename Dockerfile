# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install the dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port that the app will run on
EXPOSE 8000

RUN alembic upgrade heads
# Set environment variable to prevent Python from buffering its output
ENV PYTHONUNBUFFERED=1

