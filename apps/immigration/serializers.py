from rest_framework import serializers
from .models import PassportApplication, VisaApplication, WorkPermit

class PassportApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassportApplication
        fields = '__all__'
        read_only_fields = ['reference', 'status']
    def create(self, v):
        from core.utils import generate_tracking_id
        v['user'] = self.context['request'].user
        v['reference'] = generate_tracking_id('PPT')
        return super().create(v)

class VisaApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisaApplication
        fields = '__all__'
        read_only_fields = ['reference', 'status']

class WorkPermitSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPermit
        fields = '__all__'
        read_only_fields = ['reference', 'status']
