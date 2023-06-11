from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action

from accounts.models import CustomUser
from accounts.serializers import (
    CustomUserAllFieldsSerializer,
    CustomUserCreateSerializer,
    CustomUserChangePasswordSerializer,
    CustomUserUpdateSerializer,
    CustomUserEmailOTPVerifySerializer,
    CustomUserForgotPasswordSerializer,
    CustomUserSetPasswordSerializer,
    CustomUserListSerializer
)


class CustomUserViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserAllFieldsSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == 'create':
            serializer_class = CustomUserCreateSerializer
        elif self.action == 'change_password':
            serializer_class = CustomUserChangePasswordSerializer
        elif self.action == 'verify_by_code':
            serializer_class = CustomUserEmailOTPVerifySerializer
        elif self.action == 'forgot_password':
            serializer_class = CustomUserForgotPasswordSerializer
        elif self.action == 'set_password':
            serializer_class = CustomUserSetPasswordSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            serializer_class = CustomUserUpdateSerializer
        elif self.action == 'list' or self.action == 'me' or self.action == 'retrieve':
            serializer_class = CustomUserListSerializer

        return serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(data=self.serializer_class(instance).data, status=status.HTTP_201_CREATED)

    @action(detail=True, url_path='change_password', methods=['put'])
    def change_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        if serializer.change_password():
            response_data = {'detail': 'password updated successfully!'}
        else:
            response_data = {'detail': 'something gone wrong and password NOT updated!'}
        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(methods=['get'], url_path='verify_by_code', detail=False)
    def verify_by_code(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.verify(validated_data=serializer.validated_data)
        return Response(data=CustomUserAllFieldsSerializer(instance).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='forgot_password')
    def forgot_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response(data={'detail': 'Code sent successfully!'})

    @action(methods=['post'], detail=False, url_path='set_password')
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_password()
        return Response(data={'detail': 'Password sets successfully!'})

    @action(methods=['get'], detail=False, url_path='me')
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=False, url_path='user_delete')
    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({"Success": "User deleted "}, status=status.HTTP_204_NO_CONTENT)
