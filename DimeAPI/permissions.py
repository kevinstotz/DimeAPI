from rest_framework import permissions


class IsAuthenticatedOrCreate(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        else:
            return True
        return super(permissions.IsAuthenticatedOrCreate, self).has_permission(request, view)
