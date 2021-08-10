from staff.models import Staff, StaffAcademicInfo
from django_filters import rest_framework
from django.db.models import Q


class StaffFilter(rest_framework.FilterSet):
    faculty = rest_framework.UUIDFilter(
        method="filter_faculty_designation", lookup_expr="exact"
    )
    designation = rest_framework.UUIDFilter(lookup_expr="exact")

    def filter_faculty_designation(self, queryset, name, value):
        designation = self.request.GET.get("designation")
        faculty = self.request.GET.get("faculty")
        if faculty and designation:
            queryset = Staff.objects.filter(
                Q(staff_academic_info__faculty=faculty) | Q(designation=designation)
            )
            return queryset
        if faculty:
            queryset = Staff.objects.filter(staff_academic_info__faculty=faculty)
            return queryset

    class Meta:
        model = Staff
        fields = ["designation", "faculty"]
