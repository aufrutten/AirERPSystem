from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from django.http import HttpRequest
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APITestCase

from ..admin import UserAdmin
from .. import models


class UserAdminTest(APITestCase):
    def setUp(self):
        self.site = AdminSite()
        self.user_admin = UserAdmin(models.User, self.site)

    def test_search_fields(self):
        self.assertEqual(self.user_admin.search_fields, ('email', 'first_name', 'last_name', 'birthday'))

    def test_search_help_text(self):
        self.assertEqual(self.user_admin.search_help_text, "Search fields: email, name, surname, birthday")

    def test_get_exclude(self):
        request = HttpRequest()
        self.assertEqual(self.user_admin.get_exclude(request), ())

    def test_get_readonly_fields(self):
        request = HttpRequest()
        self.assertEqual(self.user_admin.get_readonly_fields(request), ())

        user = models.User.objects.create_superuser("test@example.com", "Hellasdo2123")
        self.assertEqual(self.user_admin.get_readonly_fields(request, user), ('email', 'last_login', 'date_joined'))

    def test_get_fieldsets_create(self):
        request = HttpRequest()
        obj = None
        fieldsets = self.user_admin.get_fieldsets(request, obj)
        expected_fieldsets = (("Creation", {'fields': ('email', 'password', 'first_name', 'last_name', 'birthday', 'sex')}),)
        self.assertEqual(fieldsets, expected_fieldsets)

    def test_get_fieldsets_edit(self):
        request = HttpRequest()
        obj = get_user_model().objects.create_superuser(email='test@example.com', password='hashedpassword')
        fieldsets = self.user_admin.get_fieldsets(request, obj)
        expected_fieldsets = [("Editing", {"fields": self.user_admin.get_fields(request, obj)})]
        self.assertEqual(fieldsets, expected_fieldsets)

    def test_save_model_create_user(self):
        request = HttpRequest()
        obj = None
        form = self.user_admin.get_form(request, obj)()
        form.cleaned_data = {
            'email': 'test@example.com',
            'password': 'hashedpassword',
            'first_name': 'John',
            'last_name': 'Doe',
            'birthday': '2000-01-01',
            'sex': 'Male',
        }
        result = self.user_admin.save_model(request, obj, form, False)
        self.assertIsInstance(result, get_user_model())
        self.assertEqual(result.email, 'test@example.com')

    def test_save_model_edit_user(self):
        request = HttpRequest()
        obj = get_user_model().objects.create_superuser(email='test@example.com', password='hashedpassword')
        form = self.user_admin.get_form(request, obj, change=True)()
        form.cleaned_data = {
            'email': 'newtest@example.com',
            'password': 'newhashedpassword',
            'first_name': 'John',
            'last_name': 'Doe',
            'birthday': '2000-01-01',
            'sex': 'Male',
        }
        result = self.user_admin.save_model(request, obj, form, True)
        self.assertIsNone(result)  # save_model returns None for edit

    def test_user_admin_page(self):
        # Test that the user admin page loads successfully
        url = reverse('admin:accounts_user_changelist')
        response = self.client.get(url)
        if response.status_code == 302:
            # Follow the redirect
            redirect_url = response.url
            response = self.client.get(redirect_url)

            # Now assert the final status code
        self.assertEqual(response.status_code, 200)
