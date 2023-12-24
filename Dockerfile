# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install Tesseract and other necessary dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get clean && \
    apt-get install -y libtk8.6 \
    rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements/requirements.txt

# Run app.py when the container launches
CMD ["python", "src/main_ui.py"]

