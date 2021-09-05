from rest_framework.urls import path
from academics.frontdesk.views.faculty import (
    FacultyListAPIView,
    FacultyRetrieveAPIView,
)

urlpatterns = [
    path("frontdesk/faculty/", FacultyListAPIView.as_view()),
    path("frontdesk/faculty/<pk>/", FacultyRetrieveAPIView.as_view()),
]
