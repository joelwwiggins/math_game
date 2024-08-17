import multiprocessing

# Gunicorn config variables
workers = multiprocessing.cpu_count() * 2 + 1
bind = "0.0.0.0:80"
timeout = 120
keepalive = 5
errorlog = "-"  # Log to stderr
accesslog = None  # Disable access log
capture_output = True
loglevel = "error"