# notifications/utils.py

from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(recipient, actor, verb, target):
    """Creates a notification record."""
    
    # Get the ContentType object for the target instance
    target_content_type = ContentType.objects.get_for_model(target)
    
    # Create the notification
    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        content_type=target_content_type,
        object_id=target.pk,
        target=target # GenericForeignKey target field
    )