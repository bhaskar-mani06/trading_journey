release: python manage.py migrate && python manage.py check --database default
web: gunicorn trading_journal.wsgi:application