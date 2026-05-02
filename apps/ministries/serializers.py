from rest_framework import serializers
from .models import Ministry, Department, Division


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ['id', 'name', 'code']


class DepartmentSerializer(serializers.ModelSerializer):
    divisions = DivisionSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description', 'director', 'divisions']


class MinistrySerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True, read_only=True)

    class Meta:
        model = Ministry
        fields = [
            'id', 'name', 'code', 'description', 'website',
            'email', 'phone', 'departments',
        ]
