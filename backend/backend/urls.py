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
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import reverse
from django.http import HttpResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


def choose_api_view(request):
    html = f"""
    <div style="display: flex; justify-content: center; align-items: center; text-align: center; min-height: 100vh">
    <a href='{reverse('redoc')}' style='margin-right: 5%'>Redoc</a>
    <br><br>
    <a href='{reverse('swagger-ui')}'>Swagger</a>
    </div>
    """
    return HttpResponse(html)


# DEFAULTS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('health-check/', include('health_check.urls', namespace="health_check")),
]

# APPS
urlpatterns += [
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
]

# SWAGGER API
urlpatterns += [
    path('', choose_api_view),
    path('schema', SpectacularAPIView.as_view(), name='schema'),
    path('redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('swagger', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
