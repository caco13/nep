from django.contrib.auth.models import User

User.objects.create_user(
    username='admin', password='nep-system',
    is_superuser=True,
    is_staff=True,
)

User.objects.create_user(username='lab1', password='nep-lab1')
User.objects.create_user(username='lab2', password='nep-lab2')
