from rest_framework.urls import path
from academics.frontdeskofficer.viewsets.section import (
    SectionListAPIView,
    SectionRetrieveAPIView,
)

urlpatterns = [
    path("front-desk-officer/section/", SectionListAPIView.as_view()),
    path("front-desk-officer/section/<pk>/", SectionRetrieveAPIView.as_view()),
]
