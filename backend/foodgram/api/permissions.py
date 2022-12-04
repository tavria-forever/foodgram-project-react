from rest_framework import permissions


class UserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        elif view.action == 'retrieve':
            return request.user.is_authenticated
        else:
            return True
