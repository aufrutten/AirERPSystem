from unittest.mock import patch, MagicMock
from datetime import date

from django.urls import reverse
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

from social_core.exceptions import AuthForbidden

from rest_framework import serializers
from rest_framework.test import APIClient, APITestCase

from .. import utils
from ..models import User
from backend.components.OAuth2.backends import GoogleOAuth2


class LoginViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.credentials = {
            'email': 'test@example.com ',
            'password': 'Qwerty1234PASS',
        }

        self.user = {
                        "first_name": "name",
                        "last_name": "surname",
                        "birthday": "1970-01-01",
                        "sex": "Male",
                    } | self.credentials

    def test_400_login(self):
        """login with invalid email and password"""
        response = self.client.post(reverse("accounts:auth"), self.credentials, format='json')

        expected_response = {
            "email": ["Unfortunately, the email address you provided was not found"],
            "password": ["The password you provided is incorrect"]
        }

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected_response)

    def test_400_login_with_unactivated_user(self):
        """login with invalid dmail and password"""
        User.objects.create_user(**self.user)
        response = self.client.post(reverse("accounts:auth"), self.credentials, format='json')

        expected_response = {
            "email": ["Account is not yet activated, please confirm your email"],
        }

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected_response)

    def test_400_login_incorrect_password(self):
        user = User.objects.create_user(**self.user)
        token = utils.get_token(user)
        user.activate_account(token)

        credentials = self.credentials.copy()
        credentials['password'] = '<INCORRECT_PASSWORD>'

        response = self.client.post(reverse("accounts:auth"), credentials, format='json')

        expected_response = {
            "password": ["The password you provided is incorrect"],
        }

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected_response)

    def test_200_login(self):
        user = User.objects.create_user(**self.user)
        token = utils.get_token(user)
        user.activate_account(token)

        response = self.client.post(reverse("accounts:auth"), self.credentials, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], self.credentials['email'].strip())
        self.assertEqual(len(response.data['access_token']), 228)
        self.assertEqual(len(response.data['refresh_token']), 229)

    def test_403_forbidden_user(self):
        user = User.objects.create_user(**self.user)
        token = utils.get_token(user)
        user.activate_account(token)

        response = self.client.post(reverse("accounts:auth"), self.credentials, format='json')
        response = self.client.post(reverse("accounts:auth"), self.credentials, format='json')

        expected_response = {
            "detail": "You do not have permission to perform this action."
        }

        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(response.data, expected_response)


class LogoutViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.credentials = {
            'email': 'test@example.com',
            'password': 'Qwerty1234PASS',
        }

        self.user = {
                        "first_name": "name",
                        "last_name": "surname",
                        "birthday": "1970-01-01",
                        "sex": "Male",
                    } | self.credentials

        self.user = User.objects.create_user(**self.user)
        self.token = utils.get_token(self.user)
        self.user.activate_account(self.token)

    def test_401_unauthorized_logout(self):
        response = self.client.delete(reverse("accounts:auth"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")

    def test_200_logout(self):
        self.client.post(reverse("accounts:auth"), self.credentials, format='json')
        response = self.client.delete(reverse("accounts:auth"))
        self.assertEqual(response.status_code, 204)


class CreateAccountViewTests(APITestCase):

    @staticmethod
    def get_user():
        credentials = {'email': 'test@example.com',
                       'password': 'Qwerty1234PASS'
                       }
        return {"first_name": "Name",
                "last_name": "surname",
                "birthday": "1999-01-01",
                "sex": "Male"
                } | credentials

    def test_with_valid_data(self):
        user = self.get_user()
        response = self.client.post(reverse("accounts:create"), user, format='json')

        expected_response = {
            'photo': None,
            'first_name': 'Name',
            'last_name': 'Surname',
            'birthday': '1999-01-01',
            'sex': 'Male',
            'email': 'test@example.com'
        }

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.data, expected_response)

    def test_with_already_exist_email(self):
        """Register with already exist email"""
        user = self.get_user()
        response = self.client.post(reverse("accounts:create"), user, format='json')
        self.assertEqual(response.status_code, 201)

        response = self.client.post(reverse("accounts:create"), user, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["email"][0],
            "Sorry, but this email address is already linked to another account."
        )

    def test_with_invalid_birthday(self):
        user = self.get_user()
        user["birthday"] = "1950-01-01"

        response = self.client.post(reverse("accounts:create"), user, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["birthday"][0],
            'Sorry, but you need to be under the age of {} year olds.'.format(settings.AGE_REMARK["MAX"])
        )

        user["birthday"] = "2100-01-01"
        response = self.client.post(reverse("accounts:create"), user, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["birthday"][0],
            'Your age is below the minimum required {} year olds.'.format(settings.AGE_REMARK["MIN"])
        )


class AccountActivationViewTests(APITestCase):

    def setUp(self):
        self.user_data = {
            "email": "test@email.com",
            "password": "<PASSWORD>",
            "first_name": "Firstname",
            "last_name": "Lastname",
            "sex": "M",
            "birthday": "1970-01-01",
        }

    def test_with_valid_data(self):
        user = User.objects.create_user(**self.user_data)

        data = {
            "token": utils.get_token(user),
            "uid": urlsafe_base64_encode(force_bytes(user.pk))
        }

        user = User.objects.get(email=self.user_data["email"])
        self.assertFalse(user.is_active)

        response = self.client.post(reverse("accounts:confirm"), data, format='json')

        user = User.objects.get(email=self.user_data["email"])
        self.assertTrue(user.is_active)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['access_token']), 228)
        self.assertEqual(len(response.data['refresh_token']), 229)

    def test_with_invalid_token(self):
        user = User.objects.create_user(**self.user_data)

        data = {
            "token": "<INVALID_TEST_TOKEN>",
            "uid": urlsafe_base64_encode(force_bytes(user.pk))
        }

        user = User.objects.get(email=self.user_data["email"])
        self.assertFalse(user.is_active)

        response = self.client.post(reverse("accounts:confirm"), data, format='json')

        user = User.objects.get(email=self.user_data["email"])
        self.assertFalse(user.is_active)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['token'][0], "Invalid token")

    def test_with_invalid_uid(self):
        user = User.objects.create_user(**self.user_data)

        data = {
            "token": utils.get_token(user),
            "uid": "<INVALID_TEST_UID>",
        }

        user = User.objects.get(email=self.user_data["email"])
        self.assertFalse(user.is_active)

        response = self.client.post(reverse("accounts:confirm"), data, format='json')

        user = User.objects.get(email=self.user_data["email"])
        self.assertFalse(user.is_active)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["uid"][0], "Invalid user ID")


class ResetPasswordViewTests(APITestCase):

    def setUp(self):
        self.user = {
            "first_name": "<NAME>",
            "last_name": "<NAME>",
            "sex": "Male",
            "birthday": "1970-01-01",
            "email": "name.surname@example.com",
            "password": "<PASSWORD>",
            "is_active": True}
        User.objects.create_user(**self.user)

    def test_with_many_requests_POST(self):
        request_data = {"email": self.user["email"]}
        response = self.client.post(reverse("accounts:reset-password"), request_data, format='json')
        response = self.client.post(reverse("accounts:reset-password"), request_data, format='json')

        expected_data = {
            "email": ["Cannot send reset link too frequently. Check your email or wait before requesting another one."]
        }

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected_data)

    def test_valid_POST(self):
        request_data = {"email": self.user["email"]}
        response = self.client.post(reverse("accounts:reset-password"), request_data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, request_data)

    def test_valid_PUT(self):
        user = User.objects.get(email=self.user["email"])
        check_password = "<NEW_PASSWORD>"

        request_data = {"email": self.user["email"], "password": check_password}
        response = self.client.post(reverse("accounts:auth"), request_data, format='json')
        self.assertEqual(response.status_code, 400)

        request_data = {
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
            "password": check_password
        }
        response = self.client.put(reverse("accounts:reset-password"), request_data, format='json')
        self.assertEqual(response.status_code, 201)

        request_data = {"email": self.user["email"], "password": check_password}
        response = self.client.post(reverse("accounts:auth"), request_data, format='json')
        self.assertEqual(response.status_code, 200)


class AccountViewTests(APITestCase):

    def setUp(self):
        self.credentials = {
            "email": "name.surname@example.com",
            "password": "<PASSWORD>"
        }
        self.user = {
            "first_name": "<NAME>",
            "last_name": "<LAST_NAME>",
            "sex": "Male",
            "birthday": "1970-01-01",
            "is_active": True
        } | self.credentials
        User.objects.create_user(**self.user)

    def test_account(self):
        self.client.post(reverse("accounts:auth"), self.credentials, format='json')

        response = self.client.get(reverse("accounts:me"), format='json')
        user = User.objects.get(email=self.user["email"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['photo'], None)
        self.assertEqual(response.data['first_name'], '<Name>')
        self.assertEqual(response.data['last_name'], '<Last_Name>')
        self.assertEqual(response.data['birthday'], '1970-01-01')
        self.assertEqual(response.data['sex'], 'Male')
        self.assertEqual(response.data['email'], 'name.surname@example.com')

    def test_update_account(self):
        self.client.post(reverse("accounts:auth"), self.credentials, format='json')

        request_data = {"first_name": "Hans", "password": "HELLOPASSWORD11"}
        response = self.client.put(reverse("accounts:me"), request_data, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse("accounts:auth"), self.credentials, format='json')
        self.assertEqual(response.status_code, 400)

        self.credentials["password"] = "HELLOPASSWORD11"
        response = self.client.post(reverse("accounts:auth"), self.credentials, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("accounts:me"), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], 'Hans')


class SocialAuthTests(APITestCase):

    def setUp(self):
        self.credentials = {
            "email": "name.surname@example.com",
            "password": "<PASSWORD>"
        }
        self.user = {
            "first_name": "<NAME>",
            "last_name": "<LAST_NAME>",
            "sex": "Male",
            "birthday": "1970-01-01",
            "is_active": True
        } | self.credentials
        User.objects.create_user(**self.user)

    def test_get_all_social_auth(self):
        response = self.client.get(reverse("accounts:social-auth", args=['all']), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {"client_id": settings.AVAILABLE_OAUTH_BACKENDS_IN_API})

    def test_get_available_social_auth(self):
        response = self.client.get(reverse("accounts:social-auth", args=['google-oauth2']), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"client_id": settings.AVAILABLE_OAUTH_BACKENDS_IN_API['google-oauth2']})

    def test_get_unavailable_social_auth(self):
        response = self.client.get(reverse("accounts:social-auth", args=['unavailable_social_auth']), format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, ["OAuth isn't exist"])

    def test_put_unavailable_social_auth(self):
        data = {"provider_token": "TEST_TOKEN"}
        url = reverse("accounts:social-auth", args=['unavailable_social_auth'])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'provider_token': ["OAuth isn't exist"]})

    @patch('backend.components.OAuth2.backends.GoogleOAuth2.do_auth')
    def test_register_by_access_token_success(self, mock_do_auth):
        mock_do_auth.return_value = User.objects.get(email=self.user['email'])
        backend_name = 'google-oauth2'
        url = reverse("accounts:social-auth", kwargs={'social_backend': backend_name})
        data = {'provider_token': 'Test_provider'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['email'], self.user["email"])

    @patch('backend.components.OAuth2.backends.GoogleOAuth2.do_auth')
    def test_register_by_access_token_failure(self, mock_do_auth):
        mock_do_auth.side_effect = AuthForbidden('Error message')
        backend_name = 'google-oauth2'
        url = reverse("accounts:social-auth", kwargs={'social_backend': backend_name})
        data = {'provider_token': 'Test_provider'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 400)


class GoogleOAuth2Tests(APITestCase):
    @patch('backend.components.OAuth2.backends.GoogleOAuth2.request')
    def test_get_image_from_url(self, mock_request):
        # Mock the response from the request method
        mock_response = MagicMock(status_code=200, content=b'mock_image_data')
        mock_request.return_value = mock_response

        # Create an instance of GoogleOAuth2
        google_oauth2 = GoogleOAuth2()

        # Call the get_image_from_url method
        result = google_oauth2.get_image_from_url('mock_url', 'mock_name_photo')

        # Assert that the method returns a valid InMemoryUploadedFile
        self.assertIsNotNone(result)
        self.assertEqual(result.name, 'mock_name_photo.jpg')
        self.assertEqual(result.content_type, 'image/jpeg')
        self.assertEqual(result.size, len(b'mock_image_data'))

    @patch('backend.components.OAuth2.backends.GoogleOAuth2.get_json')
    def test_get_birthday(self, mock_get_json):
        # Mock the response from the get_json method
        mock_response = {'birthdays': [{'date': {"year": 2022, "month": 1, "day": 1}}]}
        mock_get_json.return_value = mock_response

        # Create an instance of GoogleOAuth2
        google_oauth2 = GoogleOAuth2()

        # Call the get_birthday method
        result = google_oauth2.get_birthday('mock_access_token')

        # Assert that the method returns a valid date object
        self.assertEqual(result.year, 2022)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 1)

    @patch('backend.components.OAuth2.backends.GoogleOAuth2.get_json')
    def test_get_birthday_KeyError(self, mock_get_json):
        mock_response = {'birthdays': [{}]}
        mock_get_json.return_value = mock_response
        google_oauth2 = GoogleOAuth2()
        with self.assertRaises(serializers.ValidationError) as context:
            google_oauth2.get_birthday('mock_access_token')

        self.assertEqual(str(context.exception.detail[0]), "Invalid read extract date of birth from google account")

    @patch('backend.components.OAuth2.backends.GoogleOAuth2.get_json')
    def test_get_sex(self, mock_get_json):
        mock_response = {'genders': [{'formattedValue': 'Male'}]}
        mock_get_json.return_value = mock_response
        google_oauth2 = GoogleOAuth2()
        result = google_oauth2.get_sex('mock_access_token')
        self.assertEqual(result, 'Male')

    @patch('backend.components.OAuth2.backends.GoogleOAuth2.get_json')
    def test_get_sex_KeyError(self, mock_get_json):
        mock_response = {'genders': [{}]}
        mock_get_json.return_value = mock_response
        google_oauth2 = GoogleOAuth2()
        with self.assertRaises(serializers.ValidationError) as context:
            google_oauth2.get_sex('mock_access_token')

        self.assertEqual(str(context.exception.detail[0]), "Invalid read extract sex from google account")

    @patch('backend.components.OAuth2.backends.GoogleOAuth2.get_image_from_url')
    @patch('backend.components.OAuth2.backends.GoogleOAuth2.get_birthday')
    @patch('backend.components.OAuth2.backends.GoogleOAuth2.get_sex')
    def test_get_user_details(self, mock_get_sex, mock_get_birthday, mock_get_image_from_url):
        # Mock responses for dependencies
        mock_get_sex.return_value = 'Male'
        mock_get_birthday.return_value = date(2000, 1, 1)
        mock_get_image_from_url.return_value = MagicMock()

        # Create an instance of GoogleOAuth2
        google_oauth2 = GoogleOAuth2()

        # Mock response from Google
        response = {
            'picture': 'mock_picture_url',
            'email': 'test@example.com',
            'given_name': 'John',
            'family_name': 'Doe',
            'access_token': 'mock_access_token'
        }

        # Call the get_user_details method
        result = google_oauth2.get_user_details(response)

        # Assert the expected user details
        self.assertEqual(result['photo'], mock_get_image_from_url.return_value)
        self.assertEqual(result['email'], 'test@example.com')
        self.assertEqual(result['first_name'], 'John')
        self.assertEqual(result['last_name'], 'Doe')
        self.assertEqual(result['birthday'], date(2000, 1, 1))
        self.assertEqual(result['sex'], 'Male')
        self.assertTrue(result['is_active'])

        # Assert that the dependencies were called with the correct arguments
        mock_get_sex.assert_called_once_with('mock_access_token')
        mock_get_birthday.assert_called_once_with('mock_access_token')
        mock_get_image_from_url.assert_called_once_with('mock_picture_url', 'test@example.com')
