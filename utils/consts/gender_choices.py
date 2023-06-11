from django.db.models import TextChoices


class GenderChoice(TextChoices):
    MALE = 'male', 'Муж'
    FEMALE = 'female', 'Жен'
