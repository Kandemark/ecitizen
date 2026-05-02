from django.shortcuts import get_object_or_404


class OwnerFilterMixin:
    """Filter queryset to only show objects belonging to the current user."""

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and hasattr(self.model, 'user'):
            return qs.filter(user=user)
        return qs


class MultiSerializerMixin:
    """Use different serializers for different actions."""

    serializer_classes = {}

    def get_serializer_class(self):
        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


class AuditCreateMixin:
    """Attach user to model on create if 'user' or 'created_by' field exists."""

    def perform_create(self, serializer):
        user = self.request.user
        extra = {}
        if hasattr(serializer.Meta.model, 'user'):
            extra['user'] = user
        if hasattr(serializer.Meta.model, 'created_by'):
            extra['created_by'] = user
        serializer.save(**extra)
