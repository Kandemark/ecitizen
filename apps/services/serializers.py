from rest_framework import serializers
from .models import Service, ServiceCategory, EligibilityRule, RequiredDocument


class EligibilityRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EligibilityRule
        fields = '__all__'


class RequiredDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredDocument
        fields = '__all__'


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description', 'icon', 'order']


class ServiceListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    ministry_name = serializers.CharField(source='ministry.name', read_only=True)

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'slug', 'short_description', 'icon',
            'category', 'category_name', 'ministry', 'ministry_name',
            'processing_time', 'fee_kes', 'is_popular', 'is_online',
        ]


class ServiceDetailSerializer(serializers.ModelSerializer):
    category = ServiceCategorySerializer(read_only=True)
    eligibility_rules = EligibilityRuleSerializer(many=True, read_only=True)
    required_documents = RequiredDocumentSerializer(many=True, read_only=True)
    ministry_name = serializers.CharField(source='ministry.name', read_only=True)

    class Meta:
        model = Service
        fields = '__all__'
