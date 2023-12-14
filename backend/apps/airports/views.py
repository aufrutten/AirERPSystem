
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet

from . import models, serializers, filters


class AirportView(ReadOnlyModelViewSet):
    queryset = models.Airport.objects.all()
    serializer_class = serializers.AirportSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = filters.AirportFilter

    @method_decorator(cache_page(60 * 60 * 1))  # 1 hour
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
