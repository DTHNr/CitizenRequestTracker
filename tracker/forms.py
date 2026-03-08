from django import forms
from .models import Request

STAFF_FIELDS = ["title", "category", "description", "status", "priority", "assigned_to"]
CITIZEN_FIELDS = ["title", "category", "description", "priority"]


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = STAFF_FIELDS

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and not user.is_staff:
            for field_name in set(STAFF_FIELDS) - set(CITIZEN_FIELDS):
                self.fields.pop(field_name)
