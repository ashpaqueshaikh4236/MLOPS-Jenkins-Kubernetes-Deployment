# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install the required packages
RUN pip install -r requirements.txt

# Expose the port that the Flask app runs on
EXPOSE 5000

# Command to run the Flask application for production
CMD ["python", "app.py"]
