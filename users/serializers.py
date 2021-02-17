from rest_framework import serializers

from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    ''' Сериалайзер для модели CustomUser.

    Используем только необходимые поля и дополнительные именованные
    значения для настроек обязательности поля.

    '''
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        ]
        extra_kwargs = {
            'password': {'required': False},  # пароль не обязателен по ТЗ
            'email': {'required': True}  # email обязательно по ТЗ
        }


class ConfirmCodeSerializer(serializers.Serializer):
    ''' Сериалайзер для функции обновления токена. '''
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)
