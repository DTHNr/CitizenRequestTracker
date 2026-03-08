from django.db.models import Q, QuerySet

from .models import Request, StatusChange


def get_request_queryset(
    user,
    search: str = "",
    status: str = "",
    priority: str = "",
) -> QuerySet[Request]:
    """
    Single source of truth for building a filtered Request queryset.
    Used by the list view, CSV export, and the REST API.
    """
    qs = (
        Request.objects.all()
        .select_related("created_by", "assigned_to", "category")
        .order_by("-created_at")
    )

    if not user.is_staff:
        qs = qs.filter(created_by=user)

    if search:
        qs = qs.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(category__name__icontains=search)
        )

    if status:
        qs = qs.filter(status=status)

    if priority:
        qs = qs.filter(priority=priority)

    return qs


def create_request(user, cleaned_data: dict) -> Request:
    obj = Request(**cleaned_data)
    obj.created_by = user

    if not user.is_staff:
        obj.assigned_to = None
        obj.status = Request.Status.PENDING

    obj.save()

    StatusChange.objects.create(
        request=obj,
        old_status=obj.status,
        new_status=obj.status,
        changed_by=user,
        notes="Initial status on request creation",
    )

    return obj


def update_request(user, obj: Request, cleaned_data: dict) -> Request:
    """
    Update a Request, enforcing business rules:
    - Non-staff users cannot change status or assignee.
    """
    old_status = obj.status
    original_assigned_to = obj.assigned_to

    for field, value in cleaned_data.items():
        setattr(obj, field, value)

    if not user.is_staff:
        obj.status = old_status
        obj.assigned_to = original_assigned_to

    obj.save()

    if obj.status != old_status:
        StatusChange.objects.create(
            request=obj,
            old_status=old_status,
            new_status=obj.status,
            changed_by=user,
        )

    return obj
