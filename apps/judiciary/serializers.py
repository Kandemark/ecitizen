from rest_framework import serializers
from .models import CourtCase, Filing, HearingSchedule, Fine


class CourtCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtCase
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('CASE')
        return super().create(validated_data)


class FilingSerializer(serializers.ModelSerializer):
    case_number = serializers.CharField(source='case.case_number', read_only=True)

    class Meta:
        model = Filing
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('FIL')
        return super().create(validated_data)


class HearingScheduleSerializer(serializers.ModelSerializer):
    case_number = serializers.CharField(source='case.case_number', read_only=True)

    class Meta:
        model = HearingSchedule
        fields = '__all__'


class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fine
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('FINE')
        return super().create(validated_data)
