from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions are only allowed to the owner of the movie.
        return obj.created_by == request.user
        
class DebugPermission(permissions.BasePermission):
    """
    Permission class that logs detailed authentication information
    and then allows read-only access for unauthenticated users.
    """
    def has_permission(self, request, view):
        # Print debug information
        print(f"\nDEBUG PERMISSION CHECK")
        print(f"User: {request.user}")
        print(f"Authenticated: {request.user.is_authenticated}")
        print(f"Method: {request.method}")
        
        # Get auth headers
        auth_headers = {k: v for k, v in request.headers.items() 
                      if k.upper() in ['AUTHORIZATION', 'COOKIE', 'X-CSRFTOKEN']}
        print(f"Auth Headers: {auth_headers}")
        
        # Check for session
        if hasattr(request, 'session'):
            print(f"Session Key: {request.session.session_key}")
        
        # Allow read-only access (GET, HEAD, OPTIONS) for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # For write operations, require authentication
        return request.user and request.user.is_authenticated