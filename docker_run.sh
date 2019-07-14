#!/bin/bash
set -e
HOMEDIR="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONF="$HOMEDIR/conf/gunicorn_conf.py"
NAME="$(basename $HOMEDIR)"
cd $HOMEDIR
echo $CONF
DJANGO_SETTINGS_MODULE="callowaysite.settings"
python manage.py migrate --noinput
exec gunicorn --config $CONF wsgi:application $@
