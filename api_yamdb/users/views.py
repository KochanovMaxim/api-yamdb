from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAdmin
from .serializers import (
    AdminUserSerializer,
    SignupSerializer,
    TokenSerializer,
    UserMeSerializer,
)

User = get_user_model()


class SignupView(APIView):
    """Регистрация пользователя и отправка кода подтверждения."""
    permission_classes = []

    def post(self, request):
        """Создаёт пользователя или переотправляет код подтверждения."""
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        email = serializer.validated_data['email']

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.email != email:
                return Response(
                    {
                        'email': (
                            'Этот email уже используется другим пользователем.'
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        elif User.objects.filter(email=email).exists():
            return Response(
                {'email': 'Этот email уже используется другим пользователем.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        else:
            user = User.objects.create_user(
                username=username,
                email=email
            )

        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return Response(
            {'username': username, 'email': email},
            status=status.HTTP_200_OK
        )


class TokenView(APIView):
    """Получение JWT-токена по коду подтверждения."""
    permission_classes = []

    def post(self, request):
        """Выдаёт JWT-токен при корректном коде подтверждения."""
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']

        user = User.objects.filter(username=username).first()
        if not user:
            return Response(
                {'username': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                {'confirmation_code': 'Неверный код'},
                status=status.HTTP_400_BAD_REQUEST
            )

        token = AccessToken.for_user(user)

        return Response({'token': str(token)})


class UserMeView(APIView):
    """Просмотр и редактирование текущего пользователя."""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """Возвращает данные текущего пользователя."""
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        """Частично обновляет профиль текущего пользователя."""
        serializer = UserMeSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """CRUD-операции с пользователями (только для администратора)."""
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_serializer_class(self):
        return AdminUserSerializer
