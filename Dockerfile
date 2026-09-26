FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=folp.container_settings

WORKDIR /app
COPY requirements.lock.txt requirements-container.txt ./
RUN pip install --no-cache-dir -r requirements-container.txt

RUN useradd --create-home app
COPY --chown=app:app . .
RUN mkdir -p /app/data /app/staticfiles && chown -R app:app /app
USER app

# Build-time key is only used to collect public static assets, never at runtime.
RUN DJANGO_SECRET_KEY=static-asset-build-only python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["sh", "docker-entrypoint.sh"]
