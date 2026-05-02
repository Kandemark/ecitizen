from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Service


class ServiceFilter(filters.FilterSet):
    ministry = filters.NumberFilter(field_name='ministry_id')
    county = filters.CharFilter(field_name='counties__code')
    category = filters.NumberFilter(field_name='category_id')
    min_fee = filters.NumberFilter(field_name='fee_kes', lookup_expr='gte')
    max_fee = filters.NumberFilter(field_name='fee_kes', lookup_expr='lte')
    is_free = filters.BooleanFilter(method='filter_free')
    is_online = filters.BooleanFilter()
    is_popular = filters.BooleanFilter()
    q = filters.CharFilter(method='filter_search')

    def filter_free(self, queryset, name, value):
        if value:
            return queryset.filter(fee_kes=0)
        return queryset

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(short_description__icontains=value)
            | Q(category__name__icontains=value)
            | Q(ministry__name__icontains=value)
        ).distinct()

    class Meta:
        model = Service
        fields = [
            'ministry', 'county', 'category',
            'is_online', 'is_popular', 'is_free',
            'min_fee', 'max_fee',
        ]
