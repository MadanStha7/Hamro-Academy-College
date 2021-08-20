from rest_framework.urls import path
from onlineclass.frontdeskofficer.viewsets.online_class import (
    OnlineClassListAPIView,
)

urlpatterns = [
    path("frontdesk/online-class/", OnlineClassListAPIView.as_view()),
]
