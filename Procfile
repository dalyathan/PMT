release: pip install /django-rest-authemail
release: python3 manage.py makemigrations --noinput
release: python3 manage.py collectstatic --noinput
release: python3 manage.py migrate --noinput
web: gunicorn backtools.wsgi --log-file -
