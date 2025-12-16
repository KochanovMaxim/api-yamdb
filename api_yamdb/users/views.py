from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from api.permissions import IsAdmin
from api.serializers import (
    UserSerializer,
    SignupSerializer,
    TokenSerializer,
)


User = get_user_model()


class SignupView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class TokenView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        user = validated_data['user']

        token = AccessToken.for_user(user)
        return Response({'token': str(token)})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated],
        url_path='me',
        url_name='me'
    )
    def get_or_update_me(self, request):
        user = request.user

        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            request_data = request.data.copy()
            request_data['role'] = user.role

            serializer = self.get_serializer(
                user,
                data=request_data,
                partial=True,
                context=self.get_serializer_context()
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
