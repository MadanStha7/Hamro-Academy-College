import django_filters
from student.models import StudentInfo, StudentAcademicDetail, PreviousAcademicDetail, StudentDocument


class StudentFilter(django_filters.rest_framework.FilterSet):
    grade = django_filters.UUIDFilter(field_name='student_academic_detail__grade__id',  lookup_expr='exact')
    section = django_filters.UUIDFilter(field_name='student_academic_detail__section__id',  lookup_expr='exact')
    faculty = django_filters.UUIDFilter(field_name='student_academic_detail__faculty__id',  lookup_expr='exact')

    class Meta:
        model = StudentInfo
        fields = ["grade", "section", "faculty"]


class PreviousAcademicFilter(django_filters.rest_framework.FilterSet):
    student = django_filters.UUIDFilter(field_name='student__id', lookup_expr='exact')

    class Meta:
        model = PreviousAcademicDetail
        fields= ["student"]


class StudentDocumentFilter(django_filters.rest_framework.FilterSet):
    student = django_filters.UUIDFilter(field_name='student__id', lookup_expr='exact')

    class Meta:
        model = StudentDocument
        fields = ["student"]


class StudentAcademicFilter(django_filters.rest_framework.FilterSet):
    student = django_filters.UUIDFilter(field_name='student__id', lookup_expr='exact')

    class Meta:
        model = StudentAcademicDetail
        fields= ["student"]

