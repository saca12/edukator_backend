from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedOrCreate(BasePermission):
    """
    Allow unauthenticated POST requests for object creation (e.g. registration),
    but require authentication for all other methods.
    """

    def has_permission(self, request, view) -> bool:
        if request.method == "POST" and not request.user.is_authenticated:
            return True
        return bool(request.user and request.user.is_authenticated)


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission allowing owners to edit; others have read-only access.
    The object is expected to have a `user` or `student` attribute.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if not user or not user.is_authenticated:
            return False

        if hasattr(obj, "user"):
            return obj.user == user
        if hasattr(obj, "student"):
            return obj.student.user == user
        return False

