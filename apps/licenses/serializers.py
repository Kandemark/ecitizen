from rest_framework import serializers
from .models import BusinessLicense, ProfessionalCertification


class BusinessLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessLicense
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('BL')
        return super().create(validated_data)


class ProfessionalCertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalCertification
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('PC')
        return super().create(validated_data)
