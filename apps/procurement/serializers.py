from rest_framework import serializers
from .models import TenderNotice, Bid, Contract


class TenderNoticeSerializer(serializers.ModelSerializer):
    ministry_name = serializers.CharField(source='ministry.name', read_only=True)

    class Meta:
        model = TenderNotice
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['reference'] = generate_tracking_id('TND')
        return super().create(validated_data)


class BidSerializer(serializers.ModelSerializer):
    tender_title = serializers.CharField(source='tender.title', read_only=True)

    class Meta:
        model = Bid
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('BID')
        return super().create(validated_data)


class ContractSerializer(serializers.ModelSerializer):
    tender_title = serializers.CharField(source='tender.title', read_only=True)

    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['reference'] = generate_tracking_id('CNT')
        return super().create(validated_data)
