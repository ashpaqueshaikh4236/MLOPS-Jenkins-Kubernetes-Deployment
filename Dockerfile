FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . .

# Use the .env file to pass environment variables
COPY .env /app/.env

# Set environment variables
RUN export $(cat .env | xargs)

# Install dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]
