
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

class Gift(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='gifts',
        null=True
    )
    countdown_date = models.DateTimeField(null=True)

    class Meta:
        permissions = [
            ("can_view_gift", "Can view gift details"),
        ]
    def __str__(self):
        return self.name
    
    

class GiftCountdown(models.Model):
    gift_name = models.CharField(max_length=100, null=True)
    gift_description = models.TextField(null=True)
    countdown_date = models.DateTimeField(null=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gift_images/', blank=True, null=True)
    video = models.FileField(upload_to='gift_videos/', blank=True, null=True)
    def __str__(self):
        return f"{self.gift_name} for {self.recipient.username}"

    def is_available(self):
        # Check if the countdown date has passed
        return timezone.now() >= self.countdown_date
