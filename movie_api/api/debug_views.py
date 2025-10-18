from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt

@api_view(['GET'])
@ensure_csrf_cookie
def get_csrf_token(request):
    """
    This view does nothing but set the CSRF cookie.
    It's useful for frontend apps that need to get a CSRF token.
    """
    return Response({
        'detail': 'CSRF cookie set',
        'authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None
    })

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def debug_auth_status(request):
    """
    Debug view to check authentication status without any permission restrictions
    """
    if request.user.is_authenticated:
        user = request.user
        return Response({
            'is_authenticated': True,
            'username': user.username,
            'user_id': user.id,
            'email': user.email,
        })
    else:
        return Response({
            'is_authenticated': False,
            'message': 'User is not authenticated'
        })

@api_view(['GET', 'DELETE'])
@csrf_protect
@permission_classes([permissions.IsAuthenticated])
def debug_delete_auth(request):
    """
    This view helps debug DELETE authentication issues.
    It simulates a delete operation but just returns authentication info.
    """
    # Get auth details
    auth_method = "Unknown"
    headers = {k: v for k, v in request.headers.items() 
               if k.upper() in ['AUTHORIZATION', 'COOKIE', 'X-CSRFTOKEN']}
    
    if hasattr(request, '_auth'):
        auth_method = str(type(request._auth))
    elif hasattr(request, 'auth'):
        auth_method = str(type(request.auth))
    
    # Print debug info to server console
    print(f"DEBUG - Auth headers: {headers}")
    print(f"DEBUG - User authenticated: {request.user.is_authenticated}")
    if request.user.is_authenticated:
        print(f"DEBUG - Username: {request.user.username}, ID: {request.user.id}")
    print(f"DEBUG - Auth method: {auth_method}")
    print(f"DEBUG - Request method: {request.method}")
    
    # Return detailed information
    return Response({
        'authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None,
        'user_id': request.user.id if request.user.is_authenticated else None,
        'auth_method': auth_method,
        'headers_received': headers,
        'request_method': request.method,
        'session_key': request.session.session_key if hasattr(request, 'session') else None,
    })