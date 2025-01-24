FROM python:3.10
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY req.txt .
RUN pip install --no-cache-dir -r req.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wildberries.wsgi:application"]
