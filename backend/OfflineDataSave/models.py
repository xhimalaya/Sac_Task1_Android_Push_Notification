from django.db import models

# Create your models here.
class SurveyModel(models.Model):
    client_id = models.CharField(
        max_length=64,
        unique=True
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    age = models.BigIntegerField()
    location = models.JSONField()
    image = models.ImageField(upload_to="images/")

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
