FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Directorio para la base de datos SQLite (se monta como volumen)
RUN mkdir -p /var/data

EXPOSE 8000

CMD ["sh", "-c", "flask db upgrade && gunicorn app:app --bind 0.0.0.0:8000 --workers 2"]
