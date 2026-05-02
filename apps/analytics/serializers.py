from rest_framework import serializers
from .models import Dashboard, Widget, Metric


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class DashboardSerializer(serializers.ModelSerializer):
    widgets = WidgetSerializer(many=True, read_only=True)

    class Meta:
        model = Dashboard
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class DashboardListSerializer(serializers.ModelSerializer):
    widget_count = serializers.SerializerMethodField()

    class Meta:
        model = Dashboard
        fields = ['id', 'name', 'is_default', 'widget_count', 'created_at', 'updated_at']

    def get_widget_count(self, obj):
        return obj.widgets.count()


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = '__all__'
        read_only_fields = ['updated_at']
