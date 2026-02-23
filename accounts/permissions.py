from rest_framework.permissions import BasePermission


class IsStudentSelf(BasePermission):
    """
    Allow access only to the authenticated student's own resources.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # obj may be a Student or any model with a `student` or `user` attribute
        if hasattr(obj, "user"):
            return obj.user == user
        if hasattr(obj, "student"):
            return obj.student.user == user
        return False

