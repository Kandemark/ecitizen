from rest_framework import serializers
from .models import DrivingLicense, VehicleRegistration, PSVLicense, VehicleInspection


class DrivingLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrivingLicense
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('DL')
        return super().create(validated_data)


class VehicleRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleRegistration
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('VR')
        return super().create(validated_data)


class PSVLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PSVLicense
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('PSV')
        return super().create(validated_data)


class VehicleInspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleInspection
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('VIN')
        return super().create(validated_data)
