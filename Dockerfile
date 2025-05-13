# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install pip dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port your Flask app runs on
EXPOSE 5000

# Command to run your Flask app
CMD ["python", "run.py"]
