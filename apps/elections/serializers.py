from rest_framework import serializers
from .models import PollingStation, VoterRecord, Candidate


class PollingStationSerializer(serializers.ModelSerializer):
    county_name = serializers.CharField(source='county.name', read_only=True)

    class Meta:
        model = PollingStation
        fields = '__all__'


class VoterRecordSerializer(serializers.ModelSerializer):
    polling_station_name = serializers.CharField(source='polling_station.name', read_only=True)

    class Meta:
        model = VoterRecord
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('VR')
        return super().create(validated_data)


class CandidateSerializer(serializers.ModelSerializer):
    county_name = serializers.CharField(source='county.name', read_only=True)

    class Meta:
        model = Candidate
        fields = '__all__'
