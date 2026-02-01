from django.db import models


class Device(models.Model):
    device_id = models.CharField(max_length=255, db_index=True)
    endpoint = models.TextField(unique=True)

    p256dh = models.TextField()
    auth = models.TextField()

    user_agent = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.device_id
