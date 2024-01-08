import gunicorn
import os
import multiprocessing
from ipask.ipask import get_env_bool

# Set server name
gunicorn.SERVER = os.getenv("GUNICORN_SERVER") or "ipask"


#
# Server Socket
#

# The socket to bind.
# https://docs.gunicorn.org/en/stable/settings.html#bind
bind = os.getenv("GUNICORN_BIND") or "0.0.0.0:8080"

# The maximum number of pending connections.
# https://docs.gunicorn.org/en/stable/settings.html#backlog
backlog = 512


#
# Worker Processes
#

# The number of worker processes for handling requests.
# https://docs.gunicorn.org/en/stable/settings.html#workers
workers_default = 1
if get_env_bool("IPASK_PROD", "false"):
    workers_default = multiprocessing.cpu_count() * 2 + 1
workers = os.getenv("GUNICORN_WORKERS") or workers_default

# The number of worker threads for handling requests.
# https://docs.gunicorn.org/en/stable/settings.html#threads
threads = os.getenv("GUNICORN_THREADS") or 1

# The maximum number of simultaneous clients
# https://docs.gunicorn.org/en/stable/settings.html#worker-connections
worker_connections = 200

# The maximum number of requests a worker will process before restarting.
# https://docs.gunicorn.org/en/stable/settings.html#max-requests
max_requests = 1000

# The maximum jitter to add to the max_requests setting.
# https://docs.gunicorn.org/en/stable/settings.html#max-requests-jitter
max_requests_jitter = 100

# Workers silent for more than this many seconds are killed and restarted.
# https://docs.gunicorn.org/en/stable/settings.html#timeout
timeout = 20

# Timeout for graceful workers restart.
# https://docs.gunicorn.org/en/stable/settings.html#graceful-timeout
graceful_timeout = 20

# The number of seconds to wait for requests on a Keep-Alive connection.
# https://docs.gunicorn.org/en/stable/settings.html#keepalive
keepalive = 3


#
# Logging
#

# Disable redirect access logs to syslog
# https://docs.gunicorn.org/en/stable/settings.html#disable-redirect-access-to-syslog
disable_redirect_access_to_syslog = True

# The granularity of Error log outputs.
# https://docs.gunicorn.org/en/stable/settings.html#loglevel
loglevel = "info"


#
# Security
#

# The maximum size of HTTP request line in bytes.
# https://docs.gunicorn.org/en/stable/settings.html#limit-request-line
limit_request_line = 2048

# Limit the allowed size of an HTTP request header field.
# https://docs.gunicorn.org/en/stable/settings.html#limit-request-field-size
limit_request_field_size = 4095
