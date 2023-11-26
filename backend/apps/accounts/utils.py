
from django.conf import settings
from django.template.loader import render_to_string


import social_core.exceptions
from social_django.utils import psa
from rest_framework import serializers


@psa()
def register_by_access_token(request, backend):
    try:
        token = request.data.get('provider_token')
        return request.backend.do_auth(token)
    except social_core.exceptions.AuthForbidden as error:
        raise serializers.ValidationError(error)


class RenderEmail:
    """class for reset password and confirm email, render the html with their urls"""

    choices = {
        'confirm': {
            'subject': f'{settings.PROJECT_NAME} Confirm Email',
            'html_template': 'accounts/email_confirm.html'
        },
        'reset': {
            'subject': f'{settings.PROJECT_NAME} Reset Password',
            'html_template': 'accounts/reset_password.html'
        }
    }

    def __init__(self, user, choice='confirm'):
        self.user = user
        self.choice = choice
        self.option = self.choices[choice]

    def __call__(self, *args, **kwargs):
        context = {
            'user': self.user,
            'url': f"https://{settings.HOSTS.frontend}/{self.url}",
            'subject': self.option['subject'],
            'home_url': f'https://{settings.HOSTS.frontend}'
        }
        result = {
            'message': '',
            'subject': self.option['subject'],
            'html_message': render_to_string(self.option['html_template'], context)
        }
        return result

    @property
    def url(self):
        """getting url redirection"""
        token = self.user.access_token
        if self.choice == 'confirm':
            return f'account/confirm?email={self.user}&access_token={token}'
        return f'account/reset-password?email={self.user}&access_token={token}'
