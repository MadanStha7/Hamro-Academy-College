from rest_framework.urls import path
from academics.frontdeskofficer.viewsets.apply_shift import (
    ApplyShiftListAPIView,
    ApplyShiftRetrieveAPIView,
)

urlpatterns = [
    path("frontdesk/applyshift/", ApplyShiftListAPIView.as_view()),
    path("frontdesk/applyshift/<pk>/", ApplyShiftRetrieveAPIView.as_view()),
]
