from django.core.mail import send_mail
from config.celery import app


@app.task(bind=True)
def send_activation_email(self, email, code):
    send_mail(
            subject='Код Активации',
            message=f'Press in order to activate your account\n'
            f'http://127.0.0.1:8000/api/account/activate/?c={code}\n',
            from_email='dastan12151@gmail.com',
            recipient_list=[str(email).replace(' ', '')],
            fail_silently=True)
    return 'Done'
