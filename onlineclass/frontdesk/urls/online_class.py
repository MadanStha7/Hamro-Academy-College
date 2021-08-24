from rest_framework.urls import path
from onlineclass.frontdesk.views.online_class import (
    OnlineClassListAPIView,
)

urlpatterns = [
    path("frontdesk/online-class/", OnlineClassListAPIView.as_view()),
]
