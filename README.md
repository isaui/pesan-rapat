# Pesanan Rapat

Django project untuk sistem pesanan rapat.

## Setup

### Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

5. Run development server:
```bash
python manage.py runserver
```

### Production dengan Docker

1. Build image:
```bash
docker build -t pesanan-rapat .
```

2. Run container:
```bash
docker run -p 80:80 --env-file .env pesanan-rapat
```

## Tech Stack

- Django 5.1
- SQLite database
- Gunicorn (WSGI server)
- WhiteNoise (Static files)
- Docker ready

## Environment Variables

Lihat `.env.example` untuk konfigurasi yang diperlukan.
