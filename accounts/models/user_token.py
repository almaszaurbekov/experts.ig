import os
import binascii
from django.db import models
from django.utils.translation import gettext_lazy as _

from .user import CustomUser


class UserToken(models.Model):
    key = models.CharField(max_length=100, unique=True, verbose_name='User Token')
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='User'
    )
    user_agent = models.CharField(max_length=1000, null=True, blank=True)
    ip_address = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        abstract = False
        verbose_name = _('Token')
        verbose_name_plural = _('Tokens')

    def save(self, *args, **kwargs):
        if self.key is None or not self.key:
            self.key = self.generate_token()
        return super(UserToken, self).save(*args, **kwargs)

    def generate_token(self):
        return binascii.hexlify(os.urandom(30)).decode()

    def __str__(self):
        return f'{self.user.email} | {self.key}'

