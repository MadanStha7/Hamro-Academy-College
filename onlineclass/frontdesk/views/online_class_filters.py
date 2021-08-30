from django.db.models import F
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from onlineclass.frontdesk.serializers.online_class_filters import (
    OnlineclassFilterSerializer,
)
from permissions.front_desk_officer import FrontDeskPermission
from rest_framework.serializers import ValidationError
from rest_framework.response import Response

from academics.models import Class


class OnlineClassFilterListAPIView(ListAPIView):
    """Api to display grade,section list based on the faculty in online class"""

    serializer_class = OnlineclassFilterSerializer
    queryset = Class.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskPermission)
    pagination_class = None

    def get_queryset(self):

        faculty = self.request.query_params.get("faculty")
        grade = self.request.query_params.get("grade")

        # display grade if faculty is provided in query params
        if faculty:
            grade = (
                Class.objects.filter(
                    faculty__id=faculty, institution=self.request.institution
                )
                .values("grade__name", "grade__id")
                .distinct()
            )
            return grade
        # display section if grade is provided in query params
        if grade:
            section = (
                Class.objects.filter(
                    grade__id=grade, institution=self.request.institution
                )
                .values("section__id", "section__name")
                .distinct()
            )
            return section

        else:
            raise ValidationError(
                [
                    {"online_class": ["faculty or grade  is required query param"]},
                ]
            )
