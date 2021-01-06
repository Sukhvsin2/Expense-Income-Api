release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input
release: cd expenseincome

web: gunicorn expenseincome.wsgi