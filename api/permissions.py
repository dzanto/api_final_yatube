from rest_framework.permissions import BasePermission


class OwnResourcePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ('DELETE', 'PUT', 'POST', 'PATCH'):
            return request.user == obj.author
        return True


class OwnFollowerPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ('DELETE', 'PUT', 'POST', 'PATCH'):
            return request.user == obj.user
        return True
