release: python manage.py migrate --run-syncdb --fake-initial --verbosity=2 && python manage.py migrate --fake-initial
web: gunicorn trading_journal.wsgi:application