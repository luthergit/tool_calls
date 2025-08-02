
# Use Python 3.13 base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install uv package manager
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Copy application code
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Set environment variable for Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Command to run the Streamlit app
CMD ["uv", "run", "streamlit", "run", "ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
