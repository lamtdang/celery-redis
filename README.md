Tech stack: Flask + Celery + Redis



Celery start worker: 
celery -A celeryq.make_celery worker --loglevel INFO --concurrency {number_of_core}