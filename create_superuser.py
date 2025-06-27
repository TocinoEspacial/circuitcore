# create_superuser.py
from django.contrib.auth import get_user_model

User = get_user_model()

username = "daniel"
email = "pasta0868@gmail.com"
password = "123456789"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("✅ Superusuario creado con éxito.")
else:
    print("⚠️ El superusuario ya existe.")
