# Multi-stage build for smaller image size
FROM python:3.11-alpine AS builder

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-alpine

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy project files
COPY . .

# Make sure scripts are in PATH
ENV PATH=/root/.local/bin:$PATH

# Expose port
EXPOSE 80

# Run migrations and start gunicorn
CMD python manage.py migrate && gunicorn --bind 0.0.0.0:80 --workers 2 pesanan_rapat.wsgi:application
