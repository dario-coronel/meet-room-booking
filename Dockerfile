# Use official Python image
FROM python:3.11-slim

# Add Python scripts directory to PATH
ENV PATH="$PATH:/root/.local/bin"

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "src/main.py"]