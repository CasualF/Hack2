from django.core.mail import send_mail
from config.celery import app
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from datetime import datetime


@app.task(bind=True)
def send_activation_email(self, email, code):
    send_mail(
        subject='Код Активации',
        message=f'Press in order to activate your account\n'
                f'http://127.0.0.1:8000/api/account/activate/?c={code}\n',
        from_email='dastan12151@gmail.com',
        recipient_list=[email],
        fail_silently=True)
    return 'Done'


@app.task(bind=True)
def clear_tokens(self):
    BlacklistedToken.objects.filter(token__expires_at__lt=datetime.now()).delete()
    OutstandingToken.objects.filter(expires_at__lt=datetime.now()).delete()
    return 'Deleted expired tokens'
