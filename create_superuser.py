print("📣 SCRIPT EJECUTÁNDOSE")

import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if username and password and email:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print("✅ Superusuario creado con éxito.")
    else:
        print("⚠️ El superusuario ya existe.")
else:
    print("❌ Variables de entorno faltantes.")
