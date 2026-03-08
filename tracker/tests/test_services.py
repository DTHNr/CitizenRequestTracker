from django.test import TestCase

from tracker.models import Category, Request, StatusChange
from tracker import services
from users.models import CustomUser


class GetRequestQuerysetTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Water")

        self.staff = CustomUser.objects.create_user("admin", password="pass", is_staff=True)
        self.citizen = CustomUser.objects.create_user("citizen", password="pass")

        self.req1 = Request.objects.create(
            title="Leak on Main St",
            category=self.category,
            description="Pipe burst",
            created_by=self.citizen,
        )
        self.req2 = Request.objects.create(
            title="Fire hydrant",
            category=self.category,
            description="Broken",
            created_by=self.staff,
            status=Request.Status.IN_PROGRESS,
            priority=Request.Priority.HIGH,
        )

    def test_staff_sees_all(self):
        qs = services.get_request_queryset(user=self.staff)
        self.assertEqual(qs.count(), 2)

    def test_citizen_sees_own_only(self):
        qs = services.get_request_queryset(user=self.citizen)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.req1)

    def test_search_filters_title(self):
        qs = services.get_request_queryset(user=self.staff, search="Leak")
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.req1)

    def test_search_filters_category_name(self):
        qs = services.get_request_queryset(user=self.staff, search="water")
        self.assertEqual(qs.count(), 2)

    def test_filter_by_status(self):
        qs = services.get_request_queryset(user=self.staff, status="IN_PROGRESS")
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.req2)

    def test_filter_by_priority(self):
        qs = services.get_request_queryset(user=self.staff, priority="HIGH")
        self.assertEqual(qs.count(), 1)


class CreateRequestTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Roads")
        self.staff = CustomUser.objects.create_user("admin", password="pass", is_staff=True)
        self.citizen = CustomUser.objects.create_user("citizen", password="pass")

    def test_staff_can_set_status(self):
        obj = services.create_request(
            user=self.staff,
            cleaned_data={
                "title": "Test",
                "category": self.category,
                "description": "desc",
                "status": Request.Status.IN_PROGRESS,
                "priority": Request.Priority.HIGH,
                "assigned_to": self.staff,
            },
        )
        self.assertEqual(obj.status, Request.Status.IN_PROGRESS)
        self.assertEqual(obj.assigned_to, self.staff)

    def test_citizen_forced_to_pending(self):
        obj = services.create_request(
            user=self.citizen,
            cleaned_data={
                "title": "Test",
                "category": self.category,
                "description": "desc",
                "status": Request.Status.RESOLVED,
                "priority": Request.Priority.LOW,
                "assigned_to": self.staff,
            },
        )
        self.assertEqual(obj.status, Request.Status.PENDING)
        self.assertIsNone(obj.assigned_to)


class UpdateRequestTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electricity")
        self.staff = CustomUser.objects.create_user("admin", password="pass", is_staff=True)
        self.citizen = CustomUser.objects.create_user("citizen", password="pass")

        self.req = Request.objects.create(
            title="Power outage",
            category=self.category,
            description="No power",
            created_by=self.citizen,
        )

    def test_staff_update_creates_status_change(self):
        services.update_request(
            user=self.staff,
            obj=self.req,
            cleaned_data={
                "title": "Power outage",
                "category": self.category,
                "description": "No power",
                "status": Request.Status.IN_PROGRESS,
                "priority": Request.Priority.MEDIUM,
                "assigned_to": self.staff,
            },
        )
        self.req.refresh_from_db()
        self.assertEqual(self.req.status, Request.Status.IN_PROGRESS)

        changes = StatusChange.objects.filter(request=self.req)
        self.assertEqual(changes.count(), 1)
        self.assertEqual(changes.first().old_status, Request.Status.PENDING)
        self.assertEqual(changes.first().new_status, Request.Status.IN_PROGRESS)

    def test_citizen_cannot_change_status(self):
        services.update_request(
            user=self.citizen,
            obj=self.req,
            cleaned_data={
                "title": "Updated title",
                "category": self.category,
                "description": "Updated",
                "status": Request.Status.RESOLVED,
                "priority": Request.Priority.HIGH,
                "assigned_to": self.staff,
            },
        )
        self.req.refresh_from_db()
        self.assertEqual(self.req.status, Request.Status.PENDING)
        self.assertIsNone(self.req.assigned_to)
        self.assertEqual(self.req.title, "Updated title")

        self.assertEqual(StatusChange.objects.filter(request=self.req).count(), 0)

    def test_no_status_change_logged_when_status_unchanged(self):
        services.update_request(
            user=self.staff,
            obj=self.req,
            cleaned_data={
                "title": "Renamed",
                "category": self.category,
                "description": "Same",
                "status": Request.Status.PENDING,
                "priority": Request.Priority.MEDIUM,
                "assigned_to": None,
            },
        )
        self.assertEqual(StatusChange.objects.filter(request=self.req).count(), 0)
