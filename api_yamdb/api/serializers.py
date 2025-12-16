from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import RegexValidator
from django.http import Http404

from reviews.constants import (
    USERNAME_MAX_LENGTH, EMAIL_MAX_LENGTH, USERNAME_REGEX, FORBIDDEN_USERNAME
)
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id']
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id']
        model = Genre


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        allow_empty=False
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')

    def to_representation(self, instance):
        return TitleReadSerializer(instance, context=self.context).data


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'category', 'genre', 'rating'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, attrs):
        if self.context['request'].method != 'POST':
            return attrs

        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')

        if Review.objects.filter(author=author, title_id=title_id).exists():
            raise serializers.ValidationError(
                'Нельзя написать два отзыва на произведение'
            )

        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        required=True,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message='Недопустимые символы в имени пользователя'
            )
        ]
    )
    email = serializers.EmailField(
        required=True,
        max_length=EMAIL_MAX_LENGTH
    )

    def validate_username(self, value):
        if value == FORBIDDEN_USERNAME:
            raise serializers.ValidationError('Недопустимое имя пользователя')
        return value

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.email != email:
                raise serializers.ValidationError({
                    'email': 'Этот email используется другим пользователем.'
                })

        elif User.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                'email': 'Этот email уже используется другим пользователем.'
            })

        return data

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(
            username=validated_data['username'],
            defaults={
                'email': validated_data['email'],
                'is_active': True
            }
        )
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404('Пользователь с таким именем не существует.')

        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'}
            )

        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        required=True,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message='Недопустимые символы в имени пользователя'
            )
        ]
    )
    email = serializers.EmailField(
        required=True,
        max_length=EMAIL_MAX_LENGTH
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        extra_kwargs = {
            'username': {
                'validators': []
            }
        }

    def validate_username(self, value):
        if value == FORBIDDEN_USERNAME:
            raise serializers.ValidationError('Недопустимое имя пользователя')

        if self.instance is None:
            if User.objects.filter(username=value).exists():
                raise serializers.ValidationError(
                    'Пользователь с таким именем уже существует.'
                )

        return value

    def validate_email(self, value):
        if self.instance is None:
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError(
                    'Пользователь с таким email уже существует.'
                )

        return value

    def get_fields(self):
        fields = super().get_fields()

        request = self.context.get('request')
        if not request or not getattr(request.user, 'is_admin', False):
            fields['role'].read_only = True

        return fields
