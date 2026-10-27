from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Expense

class ExpenseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="StrongPass123!")
        self.client.login(username="testuser", password="StrongPass123!")

    def test_dashboard_loads(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_user_can_add_expense(self):
        response = self.client.post(reverse("expense_create"), {
            "title": "Lunch", "amount": "120.00", "category": "Food",
            "date": date.today().isoformat(), "note": "",
        })
        self.assertRedirects(response, reverse("expense_list"))
        self.assertEqual(Expense.objects.filter(user=self.user).count(), 1)
