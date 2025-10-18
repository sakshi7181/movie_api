"""
URL configuration for movie_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse
from rest_framework.authtoken.views import obtain_auth_token
from api.auth_views import api_login_view  # Import the login view
from api.views import register_user  # Import the register view

def home(request):
    """Home page view"""
    return HttpResponse("Welcome to Movie API!")

urlpatterns = [
    path('', home),
    path("admin/", admin.site.urls),
    path('login/', api_login_view, name='login'),  # Direct login URL
    path('register/', register_user, name='register'),  # Direct register URL
    path('api/', include('api.urls')),
    path('api/token/', obtain_auth_token, name='api_token'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # Adds login/logout to browsable API
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

