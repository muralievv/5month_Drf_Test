from celery import shared_task
from time import sleep 
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def sent_otp_email(email, code):
    print(10 * "#")
    send_mail(
    "Ваш код для регистрации",
    f"Никому не сообщайте его! {code}",
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
)
    return "SENT"

@shared_task
def water_the_flower():
    print(10 * "$")
    send_mail(
    "Напоминание!",
    "Полейте цветы!",
    settings.EMAIL_HOST_USER,
    ["nmuraliev@gmail.com"],
    fail_silently=False,
)
    return "Meow"

@shared_task
def delete_non_active():
    time_trash = timezone.now() - timedelta(minutes=30)
    unconfirmed_users = User.objects.filter(
        is_active = False,
        date_joined__lt=time_trash
    )
    count = unconfirmed_users.count()
    unconfirmed_users.delete()
    return f"Удалены {count} неподтвержденных пользователей."