from rest_framework.urls import path
from core.frontdeskofficer.viewsets.institution import InstitutionAPIView

urlpatterns = [
    path("frontdesk/institution/", InstitutionAPIView.as_view()),
]
