import multiprocessing

timeout = 120
bind = '127.0.0.1:8080'
workers = 2
threads = 5
worker_class = 'gunicorn.workers.ggevent.GeventWorker'
workers = multiprocessing.cpu_count() * 2 + 1