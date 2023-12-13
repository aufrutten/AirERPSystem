import django_filters

from .models import Airport


class AirportFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    municipality = django_filters.CharFilter(field_name='municipality', lookup_expr='icontains')
    iata_code = django_filters.CharFilter(field_name='iata_code', lookup_expr='icontains')
    keywords = django_filters.CharFilter(field_name='keywords', lookup_expr='icontains')

    class Meta:
        model = Airport
        fields = ('name', 'municipality', 'iata_code', 'keywords', 'id')
