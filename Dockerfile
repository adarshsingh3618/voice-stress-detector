# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for audio + librosa)
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    portaudio19-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Run app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
