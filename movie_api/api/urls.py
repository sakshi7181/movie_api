from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, register_user
from .auth_views import api_login_view
from django.urls import path, include

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user, name='register'),
    path('login/', api_login_view, name='api_login'),
]
