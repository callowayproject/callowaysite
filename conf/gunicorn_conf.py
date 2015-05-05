import os

INSTANCE_DIR = os.path.dirname(os.path.dirname(__file__))
INSTANCE_NAME = os.path.basename(INSTANCE_DIR)
PROJECT_DIR = os.path.dirname(INSTANCE_DIR)

NAME = 'calloway'

bind = "unix:///var/run/%s.sock" % NAME
pidfile = "/var/run/%s.pid" % NAME
user = "www-data"
group = "www-data"
accesslog = "/var/log/gunicorn/%s.access.log" % NAME
errorlog = "/var/log/gunicorn/%s.error.log" % NAME
proc_name = NAME
