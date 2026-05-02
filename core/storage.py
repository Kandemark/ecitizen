from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


class OverwriteStorage(FileSystemStorage):
    """Storage that overwrites files with the same name."""

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def document_upload_path(instance, filename):
    """Generate upload path: documents/{user_id}/{app_label}/{model}/{filename}"""
    user_id = getattr(instance, 'user_id', 'system')
    app_label = instance._meta.app_label
    model_name = instance._meta.model_name
    return f'documents/{user_id}/{app_label}/{model_name}/{filename}'


def avatar_upload_path(instance, filename):
    """Generate upload path for user avatars: avatars/{user_id}/{filename}"""
    ext = filename.rsplit('.', 1)[-1] if '.' in filename else 'jpg'
    return f'avatars/{instance.user_id}/avatar.{ext}'
