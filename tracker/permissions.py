from rest_framework import permissions as drf_permissions

from .models import Request


def can_view_request(user, obj: Request) -> bool:
    """Staff can view any request; others can only view their own."""
    return user.is_staff or obj.created_by_id == user.id


def can_edit_request(user, obj: Request) -> bool:
    """Staff can edit any request; others can only edit their own."""
    return user.is_staff or obj.created_by_id == user.id


def can_change_status(user) -> bool:
    """Only staff can change status or assign requests."""
    return user.is_staff


class IsAdminOrOwner(drf_permissions.BasePermission):
    """DRF object-level permission that reuses the shared logic."""

    def has_object_permission(self, request, view, obj):
        if request.method in drf_permissions.SAFE_METHODS:
            return can_view_request(request.user, obj)
        return can_edit_request(request.user, obj)
