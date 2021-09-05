from django.urls import path
from staff.frontdesk.views.profile import FrontDeskProfileView

urlpatterns = [path("frontdesk/profile/", FrontDeskProfileView.as_view())]
