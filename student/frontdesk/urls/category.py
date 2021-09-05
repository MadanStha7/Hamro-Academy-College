from rest_framework.urls import path
from student.frontdesk.views.category import (
    StudentCategoryListAPIView1,
    ShiftCategoryRetrieveAPIView,
)

urlpatterns = [
    path("frontdesk/category/", StudentCategoryListAPIView1.as_view()),
    path("frontdesk/category/<pk>/", ShiftCategoryRetrieveAPIView.as_view()),
]
