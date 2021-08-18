from rest_framework.urls import path
from academics.frontdeskofficer.viewsets.shift import (
    ShiftListAPIView,
    ShiftRetrieveAPIView,
)

urlpatterns = [
    path("frontdesk/shift/", ShiftListAPIView.as_view()),
    path("frontdesk/shift/<pk>/", ShiftRetrieveAPIView.as_view()),
]
