# Use an official Python 3.12 runtime as a parent image
FROM python:3.12-slim

# Install system dependencies and clean up
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        imagemagick \
        python3-tk && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Upgrade pip to the latest version
RUN pip install --no-cache-dir --upgrade pip

# Install Python packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install tk-tools separately if not included in requirements.txt
RUN pip install --no-cache-dir tk-tools

# Copy the rest of the working directory contents into the container
COPY . /app

# Expose port 8501 (Streamlit's default port)
EXPOSE 8501

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
