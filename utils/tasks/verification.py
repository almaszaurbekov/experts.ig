from django.core.mail import send_mail
from django.conf import settings

# from confs import celery_app
#
#
# @celery_app.task(name="send_email_otp",
#                  bind=True,
#                  default_retry_delay=5,
#                  max_retries=1,
#                  acks_late=True)
def send_email_otp(email, code, full_name):
    print(email, "<===---- it's print in task!")
    link = f'http://localhost/accounts/?code={code}&email={email}'

    subject = "Email Verification Code From Experts.ig!"

    body = f"Здравствуйте, {full_name}!\nДля активации аккаунта пройдите по нашей ссылке {link} \n"

    send_mail(
        subject=subject,
        message=body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email, ],
        fail_silently=False
    )
