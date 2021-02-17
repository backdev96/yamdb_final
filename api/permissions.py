from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSuperUser(BasePermission):
    '''
    Works with TitleViewSet.
    '''
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser


class IsStaffPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsAdminOrReadOnly(BasePermission):
    '''
    Works with CategoryViewSet and GenreViewSet.
    '''
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            role = request.user.is_admin or request.user.is_superuser
            return role

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            role = request.user.is_admin or request.user.is_superuser
            return role


class IsAuthorOrAdminOrModerator(BasePermission):
    '''
    Works with ReviewViewSet and CommentViewSet.
    '''
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            role = (request.user.is_admin
                    or request.user.is_moderator
                    or obj.author == request.user)
            return role
        elif request.method == "GET":
            return True
