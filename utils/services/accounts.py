import random
import binascii
import os
from django.core.cache import cache
from django.contrib.auth import authenticate

from accounts.models import CustomUser
from utils.tasks import send_email_otp


def check_password(email: str, password: str) -> bool:
    user = authenticate(username=email, password=password)

    if user is None or not user:
        return False
    elif isinstance(user, CustomUser):
        return True


#  ========= Ниже часть по отправке кода на email для верификации ========== ========== ========== ==========
def set_code_to_email(email: str, count: int):
    # code = str(random.randint(1000, 9999))
    code = binascii.hexlify(os.urandom(15)).decode()
    key = '{}_code'.format(email)
    count += 1
    cache.set(key, {'code': code, 'count': count}, 20 * 60)
    return code


def send_email_code(email_to: str, full_name: str):
    key = '{}_code'.format(email_to)
    old = cache.get(key)
    if old:
        cache.delete(key)
        count = old['count']
        if count > 5:
            return False
        else:
            code = set_code_to_email(email_to, count)
            str_code = str(code)

            print(email_to, str_code, full_name,
                  '<<<----- DATA for send_email_otp method --- ',
                  len([email_to, str_code, full_name]))

            send_email_otp(email_to, str_code, full_name)
            return code
    else:
        code = set_code_to_email(email_to, 0)
        str_code = str(code)

        print(email_to, str_code, full_name,
              '<<<----- DATA for send_email_otp method --- ',
              len([email_to, str_code, full_name]))

        send_email_otp(email_to, str_code, full_name)
        return code


def is_code_correct(email, code):
    key = '{}_code'.format(email)
    correct_code = cache.get(key)
    try:
        if correct_code['code'] == code:
            cache.delete(key)
            cache.set(key, {'code': correct_code['code'], 'count': correct_code['count'], 'check': True}, 5 * 60)
            return True
    except Exception as ex:
        print('Exception error!!!')
        print(ex)
        return False
