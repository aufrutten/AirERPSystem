"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, re_path, include
from rest_framework_simplejwt.views import TokenRefreshView

from . import views


app_name = 'accounts'

urlpatterns = [
    path('me', views.AccountView.as_view({"get": "retrieve", "delete": "destroy", "put": "partial_update"}), name='me'),
    path('login', views.AccountLoginView.as_view(), name='login'),
    path('logout', views.AccountLogoutView.as_view(), name='logout'),
    path('confirm', views.AccountConfirmView.as_view(), name='confirm'),
    path('register', views.CreateAccountView.as_view({"post": "create"}), name='create'),
    path('reset-password', views.ResetPasswordView.as_view(), name='reset-password'),
]

# JWT Default views
urlpatterns += [path('token/refresh', TokenRefreshView.as_view(), name='token_refresh')]

# Social Authentication
urlpatterns += [path('login/social/<path:backend>', views.AccountSocialLoginView.as_view(), name='social-auth')]
