# Dockerfile

# 1. Base image
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app


# 3. Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
    
# 3.1 Install MariaDB client library
RUN apt-get update && apt-get install -y gcc libmariadb-dev

# 4. Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy project files
COPY . .

# 6. Collect static files (optional, if you have them)
RUN python manage.py collectstatic --noinput

# 7. Run migrations (optional)
# (Handled later separately)

# 8. Command to run the server
CMD ["gunicorn", "django_project.wsgi:application", "--bind", "0.0.0.0:8000"]
