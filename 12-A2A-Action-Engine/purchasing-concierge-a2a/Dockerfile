# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml ./
COPY purchasing_concierge_ui.py ./
COPY purchasing_concierge ./purchasing_concierge/

# Install uv
RUN pip install uv

# Install Python dependencies
RUN uv pip install --system --no-cache \
    "a2a-sdk>=0.2.16" \
    "google-adk==1.15.1" \
    "gradio>=5.38.2" \
    "python-dotenv"

# Expose port 8080 (Cloud Run default)
EXPOSE 8080

# Set environment variable for Gradio
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=8080

# Run the application
CMD ["python", "purchasing_concierge_ui.py"]
