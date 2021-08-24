from rest_framework.urls import path
from core.frontdesk.views.institution import InstitutionAPIView

urlpatterns = [
    path("frontdesk/institution/", InstitutionAPIView.as_view()),
]
