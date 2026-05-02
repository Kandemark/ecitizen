from rest_framework import serializers
from .models import County, SubCounty, Ward, Village, Constituency


class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = ['id', 'name', 'code', 'ward']


class WardSerializer(serializers.ModelSerializer):
    villages = VillageSerializer(many=True, read_only=True)

    class Meta:
        model = Ward
        fields = ['id', 'name', 'code', 'sub_county', 'villages']


class SubCountySerializer(serializers.ModelSerializer):
    wards = WardSerializer(many=True, read_only=True)

    class Meta:
        model = SubCounty
        fields = ['id', 'name', 'code', 'county', 'wards']


class ConstituencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Constituency
        fields = ['id', 'name', 'code', 'county', 'mp_name']


class CountySerializer(serializers.ModelSerializer):
    sub_counties = SubCountySerializer(many=True, read_only=True)
    constituencies = ConstituencySerializer(many=True, read_only=True)

    class Meta:
        model = County
        fields = [
            'id', 'code', 'name', 'capital', 'governor', 'population',
            'area_sqkm', 'sub_counties', 'constituencies',
        ]
