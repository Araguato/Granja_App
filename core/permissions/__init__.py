from rest_framework import permissions

class HasGroupPermission(permissions.BasePermission):
    \"\"\"
    Permission class to check if user has required group membership.
    """
    
    def has_permission(self, request, view):
        # Get the required groups for the current action
        required_groups = getattr(view, 'required_groups', {})
        
        # Allow superusers to do anything
        if request.user.is_superuser:
            return True
            
        # Get user's groups
        user_groups = set(request.user.groups.values_list('name', flat=True))
        
        # Check if user has any of the required groups
        for group_name in required_groups.get(view.action, []):
            if group_name in user_groups:
                return True
                
        return False

class IsOwnerOrAdmin(permissions.BasePermission):
    \"\"\"
    Permission class to check if user is the owner of an object or admin.
    """
    
    def has_object_permission(self, request, view, obj):
        # Allow read permissions to any request
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Allow write permissions only to the owner or admin
        return obj.responsable == request.user or request.user.is_staff
