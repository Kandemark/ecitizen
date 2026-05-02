from rest_framework import serializers
from .models import TitleDeed, LandSearch, Transfer


class TitleDeedSerializer(serializers.ModelSerializer):
    county_name = serializers.CharField(source='county.name', read_only=True)

    class Meta:
        model = TitleDeed
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('TD')
        return super().create(validated_data)


class LandSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandSearch
        fields = '__all__'
        read_only_fields = ['reference', 'status', 'search_date', 'search_result']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('LS')
        return super().create(validated_data)


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'
        read_only_fields = ['reference', 'status']

    def create(self, validated_data):
        from core.utils import generate_tracking_id
        validated_data['user'] = self.context['request'].user
        validated_data['reference'] = generate_tracking_id('LTR')
        return super().create(validated_data)
