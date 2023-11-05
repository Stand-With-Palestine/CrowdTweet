"""Gunicorn *development* config file"""
from os import getenv
from dotenv import load_dotenv
load_dotenv()

if getenv('ENVIRONMENT') == 'prod':
    # Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
    wsgi_app = "main.wsgi:application"
    # The number of worker processes for handling requests
    workers = 3
    # The socket to bind
    bind = "0.0.0.0:=8000"
    # Write access and error info to /tmp
    accesslog = error_log = "/tmp/gunicorn.log"
    # Redirect stdout/stderr to log file
    capture_output = True
    # Set timeout for gunicorn
    timeout = 120
    # PID file so you can easily fetch process ID
    pidfile = "/tmp/dev.pid"
    # Hot Reload (Remove when migrating to new env)
    reload = True
    # Run process in the background (Remove when migrating to new env)
    daemon = True
elif getenv('ENVIRONMENT') == 'test':
    # Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
    wsgi_app = "main.wsgi:application"
    # The granularity of Error log output
    loglevel = "debug"
    # The number of worker processes for handling requests
    workers = 3
    # The socket to bind
    bind = "0.0.0.0:4000"
    # Write access and error info to /tmp
    accesslog = error_log = "/tmp/gunicorn.log"
    # Redirect stdout/stderr to log file
    capture_output = True
    # Set timeout for gunicorn
    timeout = 120
    # PID file so you can easily fetch process ID
    pidfile = "/tmp/dev.pid"
    # Hot Reload (Remove when migrating to new env)
    reload = True
    # Run process in the background (Remove when migrating to new env)
    daemon = True
else:
    # Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
    wsgi_app = "main.wsgi:application"
    # The granularity of Error log outputs
    loglevel = "debug"
    # The number of worker processes for handling requests
    workers = 3
    # The socket to bind
    bind = "0.0.0.0:4000"
    # Write access and error info to /tmp
    accesslog = error_log = "/tmp/gunicorn.log"
    # Redirect stdout/stderr to log file
    capture_output = True
    # Set timeout for gunicorn
    timeout = 120
    # PID file so you can easily fetch process ID
    pidfile = "/tmp/dev.pid"
    # hot reload the worker
    reload = True
