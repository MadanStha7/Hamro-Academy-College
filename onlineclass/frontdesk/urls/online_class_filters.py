from rest_framework.urls import path
from onlineclass.frontdesk.views.online_class_filters import (
    OnlineClassFilterListAPIView,
)


urlpatterns = [
    path("frontdesk/online-class-filter/", OnlineClassFilterListAPIView.as_view()),
]
