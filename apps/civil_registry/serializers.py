from rest_framework import serializers
from .models import BirthCertificate, DeathCertificate, MarriageCertificate


class BirthCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BirthCertificate
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('BC')
        return super().create(validated_data)


class DeathCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeathCertificate
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('DC')
        return super().create(validated_data)


class MarriageCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarriageCertificate
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('MC')
        return super().create(validated_data)
