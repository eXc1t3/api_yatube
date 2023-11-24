from rest_framework import permissions


class AuthorPermission(permissions.BasePermission):

    message = 'Правка чужого контента запрещена!'

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
