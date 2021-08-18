from django.urls import path
from staff.frontdeskofficer.viewsets.profile import FrontDeskOfficerProfileView

urlpatterns = [path("frontdesk/profile/<pk>/", FrontDeskOfficerProfileView.as_view())]
