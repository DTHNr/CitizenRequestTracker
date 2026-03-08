from django.test import TestCase

from tracker.models import Category, Request
from tracker.permissions import can_view_request, can_edit_request, can_change_status
from users.models import CustomUser


class PermissionTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Roads")

        self.staff = CustomUser.objects.create_user("admin", password="pass", is_staff=True)
        self.citizen = CustomUser.objects.create_user("citizen", password="pass")
        self.other = CustomUser.objects.create_user("other", password="pass")

        self.req = Request.objects.create(
            title="Pothole",
            category=self.category,
            description="Big hole",
            created_by=self.citizen,
        )

    def test_staff_can_view_any(self):
        self.assertTrue(can_view_request(self.staff, self.req))

    def test_owner_can_view_own(self):
        self.assertTrue(can_view_request(self.citizen, self.req))

    def test_other_cannot_view(self):
        self.assertFalse(can_view_request(self.other, self.req))

    def test_staff_can_edit_any(self):
        self.assertTrue(can_edit_request(self.staff, self.req))

    def test_owner_can_edit_own(self):
        self.assertTrue(can_edit_request(self.citizen, self.req))

    def test_other_cannot_edit(self):
        self.assertFalse(can_edit_request(self.other, self.req))

    def test_staff_can_change_status(self):
        self.assertTrue(can_change_status(self.staff))

    def test_citizen_cannot_change_status(self):
        self.assertFalse(can_change_status(self.citizen))
