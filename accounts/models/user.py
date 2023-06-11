from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from utils.models import AbstractUUID, AbstractTimeTracker
from utils.consts import GenderChoice
from accounts.manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin, AbstractUUID, AbstractTimeTracker):
    first_name = models.CharField(
        max_length=255,
        verbose_name=_('Name')
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name=_('Surname'),
        null=True,
        blank=True,
    )
    phone_regex = RegexValidator(
        regex=r'^\+?7?\d{10,23}$',
        message="Номер телефона ДОЛЖЕН быть в формате: '+71112223344'. "
                "Максимальное кол-во символов 24 (из них первые два '+7')."
    )
    phone = models.CharField(
        unique=True,
        max_length=24,
        validators=[phone_regex],
        verbose_name=_('Phone')
    )
    email = models.EmailField(
        unique=True,
        max_length=255,
        verbose_name=_('Email')
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name=_('is_active')
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('is_staff')
    )
    avatar = models.ImageField(
        upload_to='uploads/user_avatars/',
        blank=True,
        null=True,
        verbose_name=_('Avatar')
    )
    gender = models.CharField(
        choices=GenderChoice.choices,
        max_length=6,
        blank=True,
        null=True,
        verbose_name=_('Gender')
    )

    REQUIRED_FIELDS = ['phone']

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.email} | {self.first_name} {self.last_name}'
