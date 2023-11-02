"""Gunicorn *development* config file"""
import os

if os.getenv('ENVIRONMENT') == 'prod':
    # Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
    wsgi_app = "main.wsgi:application"
    # The granularity of Error log outputs
    loglevel = "debug"
    # The number of worker processes for handling requests
    workers = 3
    # The socket to bind
    bind = "0.0.0.0:4000"
    # Write access and error info to /var/log
    accesslog = error_log = "/var/log/gunicorn/dev.log"
    # Redirect stdout/stderr to log file
    capture_output = True
    # Set timeout for gunicorn
    timeout = 120
    # PID file so you can easily fetch process ID
    pidfile = "/var/run/gunicorn/dev.pid"
elif os.getenv('ENVIRONMENT') == 'test':
    # Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
    wsgi_app = "main.wsgi:application"
    # The granularity of Error log outputs
    loglevel = "debug"
    # The number of worker processes for handling requests
    workers = 3
    # The socket to bind
    bind = "0.0.0.0:4000"
    # Write access and error info to /var/log
    accesslog = error_log = "/var/log/gunicorn/dev.log"
    # Redirect stdout/stderr to log file
    capture_output = True
    # Set timeout for gunicorn
    timeout = 120
    # PID file so you can easily fetch process ID
    pidfile = "/var/run/gunicorn/dev.pid"
else:
    # Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
    wsgi_app = "main.wsgi:application"
    # The granularity of Error log outputs
    loglevel = "debug"
    # The number of worker processes for handling requests
    workers = 3
    # The socket to bind
    bind = "0.0.0.0:4000"
    # Write access and error info to /var/log
    accesslog = error_log = "/var/log/gunicorn/dev.log"
    # Redirect stdout/stderr to log file
    capture_output = True
    # Set timeout for gunicorn
    timeout = 120
    # PID file so you can easily fetch process ID
    pidfile = "/var/run/gunicorn/dev.pid"
    # hot reload the worker
    reload = True
