from rest_framework import permissions


class IsAdminOrNewUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True

        return request.user.has_perm(permissions.IsAdminUser, obj=None)

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        '''
        if request.method in permissions.SAFE_METHODS:
            return True
        '''

        return obj.owner == request.user
