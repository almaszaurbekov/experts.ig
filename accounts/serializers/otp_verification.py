from rest_framework import serializers
from rest_framework.request import Request

from accounts.models import CustomUser
from utils.consts import CustomValidationError, ValidationErrorChoice
from utils.services import is_code_correct


class CustomUserEmailOTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=False)
    code = serializers.CharField(max_length=255, required=False)

    class Meta:
        fields = 'email', 'code'

    def validate(self, attrs: dict):
        request = self.context.get('request')

        if isinstance(request, Request):
            code = request.query_params.get('code') or None
            email = request.query_params.get('email') or None
        else:
            raise CustomValidationError(ValidationErrorChoice.ERROR.value)

        if code is None or email is None:
            raise CustomValidationError(ValidationErrorChoice.EMAIL_OR_CODE_NOT_FOUND.value)

        if is_code_correct(email=email, code=code):
            attrs['code'] = code
            attrs['email'] = email
        else:
            raise CustomValidationError(ValidationErrorChoice.EMAIL_OTP_INCORRECT.value)

        return attrs

    def verify(self, validated_data):
        user = CustomUser.objects.filter(email=validated_data.get('email')).first()

        if isinstance(user, CustomUser):
            user.is_active = True
            user.save(update_fields=['is_active'])
            return user
        else:
            raise CustomValidationError(ValidationErrorChoice.ERROR.value)
