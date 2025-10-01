# Use official Python image
FROM python:3.11-slim

# Add Python scripts directory to PATH
ENV PATH="$PATH:/root/.local/bin"

# Set PYTHONPATH so 'src' is recognized as a package
ENV PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the console application as a module to ensure package imports work
CMD ["python", "-m", "src.main"]