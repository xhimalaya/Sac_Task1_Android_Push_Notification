from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .serializers import SurveyBulkSerializer


class SurveyCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        # Extract lists from multipart data
        client_ids = request.data.getlist("client_id")
        names = request.data.getlist("name")
        ages = request.data.getlist("age")
        locations = request.data.getlist("location")
        images = request.FILES.getlist("image")

        is_bulk = len(ages) > 1

        if is_bulk:
            payload = []
            for i in range(len(ages)):
                payload.append(
                        {
                        "client_id": client_ids[i],
                        "name": names[i],
                        "age": ages[i],
                        "location": locations[i],
                        "image": images[i],
                    }
                )
        else:
            payload = {
                "client_id": request.data.get("client_id"),
                "name": request.data.get("name"),
                "age": request.data.get("age"),
                "location": request.data.get("location"),
                "image": request.FILES.get("image"),
            }

        serializer = SurveyBulkSerializer(
            data=payload,
            many=is_bulk
        )
        serializer.is_valid(raise_exception=True)
        result = serializer.save()

        if isinstance(result, list):
            inserted = len(result)
        else:
            inserted = 1

        failed_ids = serializer.context.get("failed_ids", [])

        return Response(
            {
                "status": "partial_success" if failed_ids else "success",
                "inserted": inserted,
                "failed_ids": failed_ids
            },
            status=status.HTTP_201_CREATED
        )
