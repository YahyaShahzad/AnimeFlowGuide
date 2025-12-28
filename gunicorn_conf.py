import multiprocessing
from config import Config

bind = '0.0.0.0:8000'
workers = Config.GUNICORN_WORKERS or (multiprocessing.cpu_count() * 2 + 1)
timeout = Config.GUNICORN_TIMEOUT
keepalive = 5
accesslog = '-'
errorlog = '-'
