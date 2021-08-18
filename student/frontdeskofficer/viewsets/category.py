from django.db.models import F
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from student.frontdeskofficer.serializer.category import StudentCategorySerializer
from permissions.front_desk_officer import FrontDeskOfficerPermission
from student.models import StudentCategory
from student.administator.custom_fiter import StudentFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.serializers import ValidationError


class StudentCategoryListAPIView1(ListAPIView):
    """Api to display a Student list in front desk officer"""

    serializer_class = StudentCategorySerializer
    queryset = StudentCategory.objects.none()
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    permission_classes = (IsAuthenticated, FrontDeskOfficerPermission)

    def get_queryset(self):
        queryset = StudentCategory.objects.filter(institution=self.request.institution)
        return queryset


class ShiftCategoryRetrieveAPIView(RetrieveAPIView):
    """Api to retreieve a  detail in front desk officer"""

    serializer_class = StudentCategorySerializer
    queryset = StudentCategory.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskOfficerPermission)

    def get_object(self):
        try:
            student_category = StudentCategory.objects.get(
                id=self.kwargs.get("pk"), institution=self.request.institution
            )
            return student_category
        except StudentCategory.DoesNotExist:
            raise ValidationError({"error": ["StudentCategory object doesn't exist!"]})
