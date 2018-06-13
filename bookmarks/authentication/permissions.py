from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from authentication.models import Post

content_type = ContentType.objects.get_for_model(Post)
permission = Permission.objects.create(
    codename='can_publish',
    name='Can Publish Posts',
    content_type=content_type,
)
