from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()


class SignupSerializer(serializers.Serializer):
    """Сериализатор регистрации пользователя."""
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Недопустимые символы в имени пользователя'
            )
        ]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Недопустимое имя пользователя')
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор получения JWT-токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserMeSerializer(serializers.ModelSerializer):
    """Сериализатор профиля текущего пользователя."""
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя для чтения."""
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
        )


class AdminUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя для администратора."""
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
