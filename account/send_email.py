from django.core.mail import send_mail


def send_activation_email(email, code):
    send_mail(
        'Код Активации',
        f'Press in order to activate your account\n{code}\n',
        'dastan12151@gmail.com',
        [email],
        fail_silently=False
    )
