from rest_framework import serializers
from .models import TaxReturn, TaxAssessment, ComplianceCertificate


class TaxReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxReturn
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('TAX')
        return super().create(validated_data)


class TaxAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxAssessment
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('TAS')
        return super().create(validated_data)


class ComplianceCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceCertificate
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('CC')
        return super().create(validated_data)
