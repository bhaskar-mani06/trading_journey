release: python manage.py migrate --run-syncdb --fake-initial
web: gunicorn trading_journal.wsgi:application