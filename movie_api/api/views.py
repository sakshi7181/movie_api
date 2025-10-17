from rest_framework import viewsets, permissions
from .models import Movie
from .serializers import MovieSerializer
from rest_framework.permissions import AllowAny


# movie_api/movies/views.py
from rest_framework import viewsets, permissions
from .models import Movie
from .serializers import MovieSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    # Optional: restrict to authenticated users:
    # permission_classes = [permissions.IsAuthenticated]

