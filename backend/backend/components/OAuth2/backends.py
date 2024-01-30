
from abc import ABC
from io import BytesIO
from datetime import date

from rest_framework import serializers
from social_core.backends import google, apple, facebook
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile


class GoogleOAuth2(google.GoogleOAuth2, ABC):
    DEFAULT_SCOPE = [
        'openid',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/user.birthday.read',
        'https://www.googleapis.com/auth/user.gender.read',
        'https://people.googleapis.com/v1/people/me'
    ]

    def get_user_details(self, response, **kwargs):
        user = dict()
        user['photo'] = self.get_image_from_url(response['picture'], response['email'])
        user['email'] = response['email']
        user['first_name'] = response.get('given_name', '')
        user['last_name'] = response.get('family_name', '')
        user['birthday'] = self.get_birthday(response['access_token'])
        user['sex'] = self.get_sex(response['access_token'])
        user['is_active'] = True
        return user

    def get_image_from_url(self, url, name_photo):
        response = self.request(url)
        if response.status_code == 200:
            image_data = response.content
            image_file = InMemoryUploadedFile(
                file=BytesIO(image_data),
                field_name=None,
                name=f'{name_photo}.jpg',
                content_type='image/jpeg',
                size=len(image_data),
                charset=None
            )
            return image_file

    def get_birthday(self, access_token):
        url = 'https://people.googleapis.com/v1/people/me?personFields=birthdays'
        headers = self.auth_headers() | {"Authorization": f"Bearer {access_token}"}
        try:
            return date(**self.get_json(url, headers=headers)['birthdays'][0]['date'])
        except KeyError:
            raise serializers.ValidationError(_('Invalid read extract date of birth from google account'))

    def get_sex(self, access_token):
        url = 'https://people.googleapis.com/v1/people/me?personFields=genders'
        headers = self.auth_headers() | {"Authorization": f"Bearer {access_token}"}
        try:
            return self.get_json(url, headers=headers)['genders'][0]['formattedValue']
        except KeyError:
            raise serializers.ValidationError(_('Invalid read extract sex from google account'))


# class AppleIdAuth(apple.AppleIdAuth, ABC):
    # TODO: Add auth by Apple
    # pass


# class FacebookOAuth2(facebook.FacebookOAuth2, ABC):
    # TODO: Add auth by Facebook
    # pass
