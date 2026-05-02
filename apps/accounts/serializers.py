from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    county_name = serializers.CharField(source='county.name', read_only=True)
    sub_county_name = serializers.CharField(source='sub_county.name', read_only=True)
    ward_name = serializers.CharField(source='ward.name', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'id_number', 'id_type', 'phone', 'gender',
            'date_of_birth', 'county', 'county_name', 'sub_county',
            'sub_county_name', 'ward', 'ward_name', 'postal_address',
            'city', 'is_verified', 'role', 'preferences',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'is_verified', 'created_at', 'updated_at']


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=8, write_only=True)
    id_number = serializers.CharField(max_length=20)
    phone = serializers.CharField(max_length=15)
    county = serializers.IntegerField(required=False)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
        )
        profile = Profile.objects.create(
            user=user,
            id_number=validated_data.get('id_number', ''),
            phone=validated_data.get('phone', ''),
            county_id=validated_data.get('county'),
        )
        return profile
