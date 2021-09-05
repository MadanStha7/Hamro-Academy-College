from rest_framework.urls import path
from academics.frontdesk.views.subject import (
    SubjectListAPIView,
    SubjectRetrieveAPIView,
)

urlpatterns = [
    path("frontdesk/subject/", SubjectListAPIView.as_view()),
    path("frontdesk/subject/<pk>/", SubjectRetrieveAPIView.as_view()),
]
