import random

from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings

# from confs import celery_app
#
#
# @celery_app.task(name="set_password_code_send_email",
#                  bind=True,
#                  default_retry_delay=5,
#                  max_retries=1,
#                  acks_late=True)
def set_password_code_send_email(email, full_name):
    code = random.randint(100000, 999999)
    key = '{}_forgot_pass_code'.format(email)
    cache.set(key, {'code': str(code), 'count': 1}, 20 * 60)

    subject = "Set Password Verification Code From Experts.ig!"

    body = f"Здравствуйте, {full_name}!\nКод для востановления пароля => {code}"

    send_mail(
        subject=subject,
        message=body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email, ],
        fail_silently=False
    )


def check_set_password_code(email, code):
    key = '{}_forgot_pass_code'.format(email)
    correct_code = cache.get(key)
    if correct_code is None:
        return 3

    try:
        print(str(correct_code['code']), '===', str(code), ' --- both results!')
        print(str(correct_code['code']) == str(code), '<<< ---- why?')
        print(correct_code['code'] == str(code), '<<< ---- or?')
        if str(correct_code['code']) == str(code):
            cache.delete(key)
            print('--- DELETED IN CACHE ---')
            return 1
        else:
            return 0
    except Exception as e:
        print(e)
        return 0
