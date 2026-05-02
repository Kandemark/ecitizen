from rest_framework import viewsets, permissions
from ..models import County, SubCounty, Ward, Village, Constituency
from ..serializers import (
    CountySerializer, SubCountySerializer,
    WardSerializer, VillageSerializer, ConstituencySerializer,
)


class CountyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = County.objects.filter(is_active=True)
    serializer_class = CountySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'code'
    lookup_value_regex = r'\d{3}'


class SubCountyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubCounty.objects.all()
    serializer_class = SubCountySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        county_code = self.request.query_params.get('county')
        if county_code:
            qs = qs.filter(county__code=county_code)
        return qs


class WardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        sub_county_id = self.request.query_params.get('sub_county')
        if sub_county_id:
            qs = qs.filter(sub_county_id=sub_county_id)
        return qs


class VillageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Village.objects.all()
    serializer_class = VillageSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        ward_id = self.request.query_params.get('ward')
        if ward_id:
            qs = qs.filter(ward_id=ward_id)
        return qs


class ConstituencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer
    permission_classes = [permissions.AllowAny]
