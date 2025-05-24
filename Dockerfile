# Dockerfile

# Use a lightweight official Python runtime as a parent image
FROM python:3.12-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Install pytest and any other direct dependencies (like your test runner)
RUN pip install pytest

# Copy the entire project directory into the container's /app directory
COPY . /app

# Set the default command to run when the container starts
CMD ["python", "main.py"]