release: python manage.py migrate --run-syncdb
web: gunicorn trading_journal.wsgi:application