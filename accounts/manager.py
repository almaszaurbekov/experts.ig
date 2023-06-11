from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        user_instance = self.model(email=email, **extra_fields)

        if password is not None:
            user_instance.set_password(password)
        else:
            raise ValueError('ERROR: User MUST have any password!')

        user_instance.save()
        return user_instance

    def _create_user(self, email, password, **extra_fields):
        user_instance = self.model(email=email, **extra_fields)
        user_instance.is_active = True
        user_instance.set_password(password)
        return user_instance.save()

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser MUST have "is_superuser" filed value True')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser MUST have "is_staff" filed value True')

        return self._create_user(email, password, **extra_fields)
