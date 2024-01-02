import gunicorn
import os
import multiprocessing

gunicorn.SERVER = os.getenv("GUNICORN_SERVER") or "ipask"
bind = os.getenv("GUNICORN_BIND") or "0.0.0.0:8080"
workers = os.getenv("GUNICORN_WORKERS") or multiprocessing.cpu_count() * 2 + 1
threads = os.getenv("GUNICORN_THREADS") or 1
disable_redirect_access_to_syslog = True
