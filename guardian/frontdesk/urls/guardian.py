from rest_framework.urls import path
from guardian.frontdesk.views.guardaininfo import (
    GuardianListAPIView,
    GuardianRetrieveAPIView,
)

urlpatterns = [
    path("frontdesk/guardian/", GuardianListAPIView.as_view()),
    path("frontdesk/guardian/<pk>/", GuardianRetrieveAPIView.as_view()),
]
