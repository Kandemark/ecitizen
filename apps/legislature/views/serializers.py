from rest_framework import serializers
from ..models import Bill, Hansard, CommitteeReport, ParliamentarySitting


class BillListSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    house_display = serializers.CharField(source='get_house_display', read_only=True)

    class Meta:
        model = Bill
        fields = ['id', 'title', 'number', 'house', 'house_display', 'sponsor',
                  'status', 'status_display', 'date_introduced', 'date_passed', 'last_updated']


class BillSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    house_display = serializers.CharField(source='get_house_display', read_only=True)

    class Meta:
        model = Bill
        fields = '__all__'


class HansardListSerializer(serializers.ModelSerializer):
    house_display = serializers.CharField(source='get_house_display', read_only=True)

    class Meta:
        model = Hansard
        fields = ['id', 'title', 'date', 'house', 'house_display', 'sitting_number', 'summary']


class HansardSerializer(serializers.ModelSerializer):
    house_display = serializers.CharField(source='get_house_display', read_only=True)

    class Meta:
        model = Hansard
        fields = '__all__'


class CommitteeReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitteeReport
        fields = ['id', 'title', 'committee_name', 'date_published', 'summary']


class CommitteeReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitteeReport
        fields = '__all__'


class ParliamentarySittingSerializer(serializers.ModelSerializer):
    house_display = serializers.CharField(source='get_house_display', read_only=True)

    class Meta:
        model = ParliamentarySitting
        fields = '__all__'
