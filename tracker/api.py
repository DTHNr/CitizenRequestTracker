from rest_framework import permissions, viewsets, filters
from rest_framework.pagination import PageNumberPagination

from .models import Request
from .serializers import RequestSerializer
from .permissions import IsAdminOrOwner
from . import services


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]
    pagination_class = StandardResultsSetPagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description", "category__name"]
    ordering_fields = ["created_at", "priority", "status"]
    ordering = ["-created_at"]

    def get_queryset(self):
        params = self.request.query_params
        return services.get_request_queryset(
            user=self.request.user,
            status=params.get("status", ""),
            priority=params.get("priority", ""),
        )

    def perform_create(self, serializer):
        serializer.instance = services.create_request(
            user=self.request.user,
            cleaned_data=serializer.validated_data,
        )

    def perform_update(self, serializer):
        serializer.instance = services.update_request(
            user=self.request.user,
            obj=serializer.instance,
            cleaned_data=serializer.validated_data,
        )
