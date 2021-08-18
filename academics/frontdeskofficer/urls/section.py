from rest_framework.urls import path
from academics.frontdeskofficer.viewsets.section import (
    SectionListAPIView,
    SectionRetrieveAPIView,
)

urlpatterns = [
    path("frontdesk/section/", SectionListAPIView.as_view()),
    path("frontdesk/section/<pk>/", SectionRetrieveAPIView.as_view()),
]
