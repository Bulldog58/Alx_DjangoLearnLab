from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model() 

class Notification(models.Model):
    recipient = models.ForeignKey(get_user_model(), related_name='notifications_received', on_delete=models.CASCADE)
    actor = models.ForeignKey(User, related_name='actions', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)  
    target_content_type = models.ForeignKey(ContentType, related_name='notifications_targeted', on_delete=models.CASCADE)
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Notification from {self.actor} to {self.recipient}: {self.verb}"