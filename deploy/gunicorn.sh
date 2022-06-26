#!/bin/bash

NAME="agrotienda"
DJANGODIR=$(dirname $(cd `dirname $0` && pwd))
SOCKFILE=/tmp/gunicorn-agrotienda.sock
LOGDIR=${DJANGODIR}/logs/gunicorn.log
USER=michael
GROUP=michael
NUM_WORKERS=5
DJANGO_WSGI_MODULE=Agro_Tienda.wsgi

rm -frv $SOCKFILE

echo $DJANGODIR

cd $DJANGODIR

exec ${DJANGODIR}/env/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=$LOGDIR
