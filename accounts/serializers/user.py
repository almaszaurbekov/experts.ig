from rest_framework import serializers

from accounts.models import CustomUser
from utils.consts import CustomValidationError, ValidationErrorChoice
from utils.services import check_password, send_email_code
from utils.tasks import set_password_code_send_email, check_set_password_code


class CustomUserAllFieldsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = 'uuid', 'first_name', 'last_name', 'phone', 'email', \
                 'avatar', 'gender', 'role', 'is_active', 'created_at', 'updated_at', 'user_offline'


class CustomUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = CustomUser
        fields = 'email', 'phone', 'first_name', 'last_name', 'avatar', 'gender', 'password'

    def create(self, validated_data):
        validated_data['is_active'] = False
        email = validated_data.get('email') or None
        password = validated_data.pop('password') or None
        if email is None:
            raise CustomValidationError(ValidationErrorChoice.EMAIL_NOT_FOUND.value)

        send_email_code(
            email,
            validated_data.get("first_name")
        )

        instance = super().create(validated_data)
        instance.set_password(password)
        instance.save()

        return instance


class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=True, help_text='Email')
    password = serializers.CharField(max_length=255, required=True, help_text='Password')

    class Meta:
        fields = 'email', 'password'

    def validate(self, attrs):
        email = attrs.get('email') or None
        password = attrs.get('password') or None

        if (email is None or password is None) or (not email or not password):
            raise CustomValidationError(ValidationErrorChoice.EMAIL_OR_PASSWORD_NOT_FOUND.value)

        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            raise CustomValidationError(ValidationErrorChoice.USER_DATA_OR_USER_NOT_FOUND.value)
        else:
            attrs['email'] = user.email
        return attrs


class CustomUserChangePasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, max_length=100)
    password = serializers.CharField(max_length=255, required=True)
    new_password1 = serializers.CharField(max_length=255, required=True)
    new_password2 = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = CustomUser
        fields = 'email', 'password', 'new_password1', 'new_password2'

    def validate(self, attrs):
        user = self.context.get('request').user
        email = attrs.get('email')
        if user is None and email is None:
            raise CustomValidationError(ValidationErrorChoice.USER_DATA_OR_USER_NOT_FOUND.value)
        elif email is None and isinstance(user, CustomUser):
            attrs.__setitem__('email', user.email)
        elif user is None:
            user = CustomUser.objects.filter(email=email).first()

        new_password1 = attrs.get('new_password1')
        new_password2 = attrs.get('new_password2')
        if new_password1 is None or new_password2 is None:
            raise CustomValidationError(ValidationErrorChoice.PAS1_or_PAS2_NOT_FOUND.value)
        elif new_password1 != new_password2:
            raise CustomValidationError(ValidationErrorChoice.PAS1_or_PAS2_NOT_EQUAL.value)

        password = attrs.get('password')
        if password is None:
            raise CustomValidationError(ValidationErrorChoice.PASSWORD_NOT_FOUND.value)
        elif not check_password(user.email, password):
            raise CustomValidationError(ValidationErrorChoice.PASSWORD_INCORRECT.value)

        attrs.__setitem__('user', user)
        return attrs

    def change_password(self):
        try:
            user = self.validated_data.get('user')
            password = self.validated_data.get('new_password1')
            user.set_password(password)
            user.save()
            return True
        except Exception as e:
            print(e.__traceback__)
            return False


class CustomUserForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('email', )

    def validate(self, attrs):
        email = attrs.get('email', None)

        if email is None:
            raise CustomValidationError(ValidationErrorChoice.EMAIL_NOT_FOUND.value)
        else:
            user = CustomUser.objects.filter(email=email).first()
            if not isinstance(user, CustomUser):
                raise CustomValidationError(ValidationErrorChoice.USER_DATA_OR_USER_NOT_FOUND.value)
            else:
                attrs['user'] = user

        return attrs

    def send_code(self):
        user = self.validated_data.get('user')
        set_password_code_send_email(
            self.validated_data.get('email'),
            f'{user.first_name} {user.last_name}'
        )


class CustomUserSetPasswordSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50, required=True, help_text='Code from your email!')
    email = serializers.EmailField(required=True, help_text='User email address!')
    new_password = serializers.CharField(max_length=255, required=True, help_text='New password data!')

    class Meta:
        fields = 'code', 'email'

    def validate(self, attrs):
        email = attrs.get('email', None)
        if email is None:
            raise CustomValidationError(ValidationErrorChoice.EMAIL_NOT_FOUND.value)
        else:
            user = CustomUser.objects.filter(email=email).first()
            if not isinstance(user, CustomUser):
                raise CustomValidationError(ValidationErrorChoice.USER_DATA_OR_USER_NOT_FOUND.value)
            else:
                attrs['user'] = user

        code = attrs.get('code')

        check = check_set_password_code(email, code)
        if check == 0:
            raise CustomValidationError(ValidationErrorChoice.EMAIL_OTP_INCORRECT.value)
        elif check == 3:
            raise CustomValidationError(ValidationErrorChoice.RESEND_OTP.value)

        return attrs

    def set_password(self):
        user = self.validated_data.get('user')
        if isinstance(user, CustomUser):
            user.set_password(self.validated_data.get('new_password'))
            user.save()


class CustomUserUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = 'first_name', 'last_name', 'phone', 'email', 'avatar', 'gender'


class CustomUserUpdateRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = 'role',
