from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from core.throttling import LoginRateThrottle, RegistrationRateThrottle
from ..models import Profile, AuditEntry
from ..serializers import UserSerializer, ProfileSerializer, RegisterSerializer


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    @action(detail=False, methods=['post'], throttle_classes=[LoginRateThrottle])
    def login(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            token = RefreshToken.for_user(user)
            AuditEntry.objects.create(
                user=user, action='api_login',
                ip_address=request.META.get('REMOTE_ADDR', ''),
            )
            return Response({
                'access': str(token.access_token),
                'refresh': str(token),
                'user': UserSerializer(user).data,
            })
        return Response({'detail': 'Invalid credentials.'}, status=401)

    @action(detail=False, methods=['post'], throttle_classes=[RegistrationRateThrottle])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.save()
            user = profile.user
            token = RefreshToken.for_user(user)
            AuditEntry.objects.create(
                user=user, action='api_register',
                ip_address=request.META.get('REMOTE_ADDR', ''),
            )
            return Response({
                'access': str(token.access_token),
                'refresh': str(token),
                'user': UserSerializer(user).data,
                'profile': ProfileSerializer(profile).data,
            }, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        return Response({'detail': 'Logged out.'})


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Profile.objects.all()
        return Profile.objects.filter(user=self.request.user)

    def get_object(self):
        if self.action in ('retrieve', 'update', 'partial_update'):
            return self.request.user.profile
        return super().get_object()

    @action(detail=False, methods=['post'])
    def upload_avatar(self, request):
        profile = request.user.profile
        if 'avatar' not in request.FILES:
            return Response({'detail': 'No image provided.'}, status=400)
        file = request.FILES['avatar']
        if file.size > 5 * 1024 * 1024:
            return Response({'detail': 'Image too large. Max 5MB.'}, status=400)
        if file.content_type not in ('image/jpeg', 'image/png', 'image/webp'):
            return Response({'detail': 'Invalid format. Use JPEG, PNG, or WebP.'}, status=400)
        profile.avatar = file
        profile.save()
        return Response({'avatar_url': request.build_absolute_uri(profile.avatar.url)})
