from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def api_login_view(request):
    """
    API login view that returns an authentication token
    """
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Generate or get token
            token, created = Token.objects.get_or_create(user=user)
            
            # Get next URL from POST data (form submission)
            next_url = request.data.get('next', '/api/movies/')
            
            # Redirect to movies API after login if there's a 'next' parameter
            if next_url:
                return redirect(next_url)
                
            # Otherwise return the token
            return JsonResponse({
                'message': 'Login successful',
                'token': token.key,
                'username': user.username
            })
        else:
            # If authentication fails, render login page with error
            next_url = request.data.get('next', '/api/movies/')
            return render(request, 'api/login.html', {
                'next_url': next_url,
                'error_message': 'Invalid username or password'
            }, status=400)
    
    # For GET requests, provide login form with next parameter
    next_url = request.GET.get('next', '/api/movies/')
    return render(request, 'api/login.html', {'next_url': next_url})