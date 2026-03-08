from django.db import IntegrityError
from django.test import TestCase

from tracker.models import Category, Request
from users.models import CustomUser


class CategoryModelTests(TestCase):
    def test_str(self):
        cat = Category.objects.create(name="Roads")
        self.assertEqual(str(cat), "Roads")

    def test_unique_name(self):
        Category.objects.create(name="Water")
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Water")


class RequestModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="General")
        self.user = CustomUser.objects.create_user("testuser", password="pass")

    def test_str(self):
        req = Request.objects.create(
            title="Fix road",
            category=self.category,
            description="Needs repair",
            created_by=self.user,
        )
        self.assertEqual(str(req), "Fix road (PENDING)")

    def test_defaults(self):
        req = Request.objects.create(
            title="Test",
            category=self.category,
            description="Desc",
            created_by=self.user,
        )
        self.assertEqual(req.status, Request.Status.PENDING)
        self.assertEqual(req.priority, Request.Priority.MEDIUM)
        self.assertIsNone(req.assigned_to)
