release: python manage.py migrate --run-syncdb --fake-initial --verbosity=2
web: gunicorn trading_journal.wsgi:application