from rest_framework.urls import path
from academics.frontdeskofficer.viewsets.class_url import (
    ClassListAPIView,
    ClassRetrieveAPIView,
)

urlpatterns = [
    path("frontdesk/class/", ClassListAPIView.as_view()),
    path("frontdesk/class/<pk>/", ClassRetrieveAPIView.as_view()),
]
