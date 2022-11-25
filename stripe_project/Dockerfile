FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /stripe_project

# Install dependencies
COPY requirements.txt /stripe_project/
RUN pip install -r requirements.txt

# Copy project
COPY . /stripe_project/

# collect static files
RUN python manage.py collectstatic --noinput

# run gunicorn
CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000