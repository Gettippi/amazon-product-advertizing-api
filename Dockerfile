# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Copy the requirements file to the container
COPY requirements.txt .

# Update pip to the latest version
RUN pip3 install --no-cache-dir --upgrade pip3

# Install the dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY app.py .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]