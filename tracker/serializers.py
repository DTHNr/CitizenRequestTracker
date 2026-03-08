from rest_framework import serializers
from .models import Category, Request


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class RequestSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source="created_by.username", read_only=True)
    assigned_to_username = serializers.CharField(source="assigned_to.username", read_only=True, default="")
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Request
        fields = [
            "id",
            "title",
            "category",
            "category_name",
            "description",
            "status",
            "priority",
            "created_by",
            "created_by_username",
            "assigned_to",
            "assigned_to_username",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and not request.user.is_staff:
            self.fields["status"].read_only = True
            self.fields["assigned_to"].read_only = True
