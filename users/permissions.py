from rest_framework import permissions


class IsModeratorPermission(permissions.BasePermission):
    ''' Класс описывает пермишены для свойства is_moderator
    объекта класса CustomUser. Свойство получено путем использования
    декоратора @property.

    '''
    def has_permission(self, request, view):
        return request.user.is_moderator


class IsAdminPermission(permissions.BasePermission):
    ''' Класс описывает пермишены для свойства is_admin
    объекта класса CustomUser. Свойство получено путем использования
    декоратора @property.

    '''
    def has_permission(self, request, view):
        return request.user.is_admin


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
    ''' Класс описывает пермишен при допуске к тому или иному объекту
    автора объекта. Если запрашивающий доступ к объекту не является автором,
    то ему разрешены только безопасные методы запроса (в частности - чтение).

    '''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
