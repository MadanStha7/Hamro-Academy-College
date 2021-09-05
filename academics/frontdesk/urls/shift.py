from rest_framework.urls import path
from academics.frontdesk.views.shift import (
    ShiftListAPIView,
    ShiftRetrieveAPIView,
)

urlpatterns = [
    path("frontdesk/shift/", ShiftListAPIView.as_view()),
    path("frontdesk/shift/<pk>/", ShiftRetrieveAPIView.as_view()),
]
