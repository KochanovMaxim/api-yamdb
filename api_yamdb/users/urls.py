from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import SignupView, TokenView, UserMeView, UserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', SignupView.as_view()),
    path('auth/token/', TokenView.as_view()),
    path('users/me/', UserMeView.as_view(), name='users-me'),
]

urlpatterns += router_v1.urls
