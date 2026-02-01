from django.urls import path
from .views import SurveyCreateView

urlpatterns = [
    path("survey/", SurveyCreateView.as_view(), name="survey-create"),
]
