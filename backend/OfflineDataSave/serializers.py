from rest_framework import serializers
from django.db import transaction
from .models import SurveyModel 

class SurveyBulkListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        success = []
        failed = []

        with transaction.atomic():
            for item in validated_data:
                client_id = item.get("client_id")

                try:
                    obj = SurveyModel.objects.create(**item)
                    success.append(obj)

                except Exception:
                    failed.append(client_id)

        self.context["failed_ids"] = failed
        return success



class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyModel
        fields = ["id", "name", "age", "location", "image", "created_at"]

class SurveyBulkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyModel
        fields = ["client_id", "name", "age", "location", "image"]
        list_serializer_class = SurveyBulkListSerializer


