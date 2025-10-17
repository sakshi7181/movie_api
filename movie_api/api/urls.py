from rest_framework.routers import DefaultRouter
from .views import MovieViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'movies', MovieViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
