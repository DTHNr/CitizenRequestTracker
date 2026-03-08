import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from .forms import RequestForm
from .models import Request
from . import services
from . import permissions as perms


def _get_filter_params(request):
    """Extract common filter params from the GET querystring."""
    return {
        "search": request.GET.get("q", "").strip(),
        "status": request.GET.get("status", "").strip(),
        "priority": request.GET.get("priority", "").strip(),
    }


@login_required
@never_cache
def request_list(request):
    params = _get_filter_params(request)
    qs = services.get_request_queryset(user=request.user, **params)

    from django.core.paginator import Paginator

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "q": params["search"],
        "status": params["status"],
        "priority": params["priority"],
        "status_choices": Request.Status.choices,
        "priority_choices": Request.Priority.choices,
    }
    return render(request, "tracker/request_list.html", context)


@login_required
@never_cache
def request_export_csv(request):
    params = _get_filter_params(request)
    qs = services.get_request_queryset(user=request.user, **params)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="citizen_requests.csv"'

    writer = csv.writer(response)
    writer.writerow(["ID", "Title", "Category", "Status", "Priority", "Created By", "Assigned To", "Created At"])

    for r in qs:
        writer.writerow([
            r.id,
            r.title,
            r.category.name,
            r.status,
            r.priority,
            r.created_by.username,
            r.assigned_to.username if r.assigned_to else "",
            r.created_at.isoformat(),
        ])

    return response


@login_required
@never_cache
def dashboard(request):
    qs = services.get_request_queryset(user=request.user)

    by_status = qs.values("status").annotate(total=Count("id")).order_by("status")
    by_priority = qs.values("priority").annotate(total=Count("id")).order_by("priority")
    by_category = qs.values("category__name").annotate(total=Count("id")).order_by("category__name")

    context = {
        "total": qs.count(),
        "by_status": by_status,
        "by_priority": by_priority,
        "by_category": by_category,
    }
    return render(request, "tracker/dashboard.html", context)


@login_required
@never_cache
def request_create(request):
    form = RequestForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        obj = services.create_request(user=request.user, cleaned_data=form.cleaned_data)
        messages.success(request, "Request created.")
        return redirect("tracker:request_detail", pk=obj.pk)

    return render(request, "tracker/request_form.html", {"form": form, "mode": "create"})


@login_required
@never_cache
def request_detail(request, pk: int):
    obj = get_object_or_404(Request.objects.select_related("created_by", "assigned_to", "category"), pk=pk)

    if not perms.can_view_request(request.user, obj):
        raise Http404()

    status_changes = obj.status_changes.select_related("changed_by")
    return render(request, "tracker/request_detail.html", {"obj": obj, "status_changes": status_changes})


@login_required
@never_cache
def request_update(request, pk: int):
    obj = get_object_or_404(Request, pk=pk)

    if not perms.can_edit_request(request.user, obj):
        raise Http404()

    form = RequestForm(request.POST or None, instance=obj, user=request.user)

    if request.method == "POST" and form.is_valid():
        obj = services.update_request(user=request.user, obj=obj, cleaned_data=form.cleaned_data)
        messages.success(request, "Request updated.")
        return redirect("tracker:request_detail", pk=obj.pk)

    return render(request, "tracker/request_form.html", {"form": form, "mode": "edit", "obj": obj})


@login_required
@never_cache
def request_delete(request, pk: int):
    obj = get_object_or_404(Request, pk=pk)

    if not perms.can_edit_request(request.user, obj):
        raise Http404()

    if request.method == "POST":
        obj.delete()
        messages.success(request, "Request deleted.")
        return redirect("tracker:request_list")

    return render(request, "tracker/request_confirm_delete.html", {"obj": obj})
