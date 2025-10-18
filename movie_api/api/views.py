from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Movie
from .serializers import MovieSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# User registration endpoint
@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    if request.method == 'GET':
        # Return the HTML page for browser access
        return render(request, 'api/register.html')
    
    # For POST requests (API calls)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # READ is public, CREATE/UPDATE requires auth
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # Support different content types
    queryset = Movie.objects.all()  # Default queryset, will be overridden by get_queryset()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def get_queryset(self):
        """
        This view returns movies filtered by user:
        - If user is authenticated, only show their own movies
        - If user is anonymous, show all public movies
        
        Add a query parameter ?all=true to see all movies
        """
        user = self.request.user
        
        # Check if the user explicitly wants to see all movies (for admins or special cases)
        show_all = self.request.query_params.get('all', 'false').lower() == 'true'
        
        if user.is_authenticated and not show_all:
            # Filter movies by the current user
            return Movie.objects.filter(created_by=user)
        else:
            # Show all movies for anonymous users or when specifically requested
            return Movie.objects.all()
            
    @action(detail=False, methods=['get'])
    def all_movies(self, request):
        """
        Endpoint to get all movies regardless of owner
        Access via: /api/movies/all_movies/
        """
        movies = Movie.objects.all()
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)

