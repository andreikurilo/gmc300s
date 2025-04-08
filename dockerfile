# Use an official lightweight Python image.
FROM python:3.11

# Set working directory in the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

RUN pip install --upgrade pip
# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY src/ .

# Expose port 8000 for FastAPI
EXPOSE 5000

# Start the FastAPI server using uvicorn
CMD ["python", "main.py"]
