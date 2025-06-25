#!/bin/bash

# Render asigna automáticamente el puerto como variable de entorno $PORT
# Así que lo usamos al iniciar el servidor
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:$PORT
