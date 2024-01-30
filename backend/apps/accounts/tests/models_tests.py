import time
from datetime import timedelta
from urllib.parse import urlparse, parse_qs

from django.core import mail
from django.utils import timezone
from rest_framework.test import APITestCase

from .. import utils
from ..models import User
from ..tasks import send_email_celery


class UserTest(APITestCase):
    """Base case (correct)"""

    def setUp(self):
        self.user_data = {
            "email": "test@email.com",
            "password": "<PASSWORD>",
            "first_name": "Firstname",
            "last_name": "Lastname",
            "sex": "M",
            "birthday": "1970-01-01",
        }

    def test_creation_user(self):
        user = User.objects.create_user(**self.user_data)

        self.assertEqual(user.email, self.user_data["email"])
        self.assertEqual(user.first_name, self.user_data["first_name"])
        self.assertEqual(user.last_name, self.user_data["last_name"])

        self.assertNotEqual(user.password, self.user_data["password"])
        self.assertEqual(
            utils.check_last_email_received(user),
            timezone.now() - timedelta(hours=1) >= user.last_email_received
        )

    def test_creation_superuser(self):
        user = User.objects.create_superuser("test2@email.com", "PASSWORD")

        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_active, True)

    def test_activate_user(self):
        user = User.objects.create_user(**self.user_data)

        token = utils.get_token(user)

        self.assertEqual(user.is_active, False)

        user.activate_account(token)

        self.assertEqual(utils.check_token(user, token), True)
        self.assertEqual(user.is_active, True)

    def test_util_get_context_for_user(self):
        user = User.objects.create_user(**self.user_data)
        url_one = "https://{frontend}/account/confirm?uid={uid}&token={token}"
        url_two = "https://{frontend}/account/reset-password?uid={uid}&token={token}"

        context_one = utils.get_context(user, url_one)
        time.sleep(2)
        context_two = utils.get_context(user, url_two)

        self.assertNotEqual(context_one['url'], context_two['url'])
        self.assertEqual(utils.check_token(user, parse_qs(urlparse(context_one['url']).query).get("token")[0]), True)
        self.assertEqual(utils.check_token(user, parse_qs(urlparse(context_two['url']).query).get("token")[0]), True)


class TestInvalidUser(APITestCase):

    def test_with_empty_email(self):
        with self.assertRaises(ValueError) as error:
            User.objects.create_user("", "<PASSWORD>")
        self.assertEqual(str(error.exception), "Users must have an email address")


class TestAsyncEmailSend(APITestCase):

    def test_email_send(self):
        args = {"recipient_list": ["TEST@example.com"]}
        result = send_email_celery.delay("TEST_SUBJECT", "TEST_MESSAGE", from_email=None, **args)

        self.assertEquals(result.get(), 1)
        self.assertTrue(result.successful())

        sent_email = mail.outbox[0]
        self.assertEqual(sent_email.subject, "TEST_SUBJECT")
        self.assertEqual(sent_email.body, "TEST_MESSAGE")
