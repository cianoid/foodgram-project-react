from rest_framework import permissions


class AnonymousOnly(permissions.BasePermission):
    message = 'Доступ запрещен'

    def has_permission(self, request, view):
        return not request.user.is_authenticated
