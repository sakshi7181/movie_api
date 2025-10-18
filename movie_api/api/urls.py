from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, register_user
from .auth_views import api_login_view
from django.urls import path, include
from .debug_views import get_csrf_token, debug_delete_auth, debug_auth_status

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user, name='register'),
    path('login/', api_login_view, name='api_login'),
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    path('debug-delete-auth/', debug_delete_auth, name='debug_delete_auth'),
    path('debug-auth-status/', debug_auth_status, name='debug_auth_status'),
]
