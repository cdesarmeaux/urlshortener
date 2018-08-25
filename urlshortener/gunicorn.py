import multiprocessing

timeout = 120
bind = ':8080'
workers = 2
threads = 5
worker_class = 'gunicorn.workers.ggevent.GeventWorker'
workers = multiprocessing.cpu_count() * 2 + 1