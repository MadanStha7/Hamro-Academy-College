import django_filters
from academics.models import ApplyShift, Class
from academics.models import SubjectGroup
from onlineclass.models import OnlineClassInfo


from academics.models import SubjectGroup
from timetable.models import TimeTable


class SubjectGroupFilter(django_filters.rest_framework.FilterSet):
    grade = django_filters.UUIDFilter(field_name="grade__id", lookup_expr="exact")
    section = django_filters.UUIDFilter(field_name="section__id", lookup_expr="exact")
    faculty = django_filters.UUIDFilter(field_name="faculty__id", lookup_expr="exact")
    subject = django_filters.UUIDFilter(field_name="subject__id", lookup_expr="exact")

    class Meta:
        model = SubjectGroup
        fields = ["grade", "section", "subject", "faculty"]


class ApplyShiftFilter(django_filters.rest_framework.FilterSet):
    grade = django_filters.UUIDFilter(field_name="grade__id", lookup_expr="exact")
    section = django_filters.UUIDFilter(field_name="section__id", lookup_expr="exact")
    faculty = django_filters.UUIDFilter(field_name="faculty__id", lookup_expr="exact")

    class Meta:
        model = ApplyShift
        fields = ["grade", "section", "faculty"]


class TimeTableFilter(django_filters.rest_framework.FilterSet):
    grade = django_filters.UUIDFilter(field_name='grade__id', lookup_expr='exact')
    section = django_filters.UUIDFilter(field_name='section__id', lookup_expr='exact')

    class Meta:
        model = SubjectGroup
        fields = ["grade", "section", "subject", "faculty"]


class TeacherTimeTableFilter(django_filters.rest_framework.FilterSet):
    grade = django_filters.UUIDFilter(field_name='grade__id', lookup_expr='exact')
    section = django_filters.UUIDFilter(field_name='section__id', lookup_expr='exact')

    class Meta:
        model = TimeTable
        fields = ["grade", "section"]


class OnlineClassFilter(django_filters.rest_framework.FilterSet):
    grade = django_filters.UUIDFilter(field_name='grade__id', lookup_expr='exact')
    section = django_filters.UUIDFilter(field_name='section__id', lookup_expr='exact')

    class Meta:
        model = OnlineClassInfo
        fields = ["grade", "section"]


class ClassFilter(django_filters.rest_framework.FilterSet):
    faculty = django_filters.UUIDFilter(field_name='faculty_id', lookup_expr='exact')
    grade = django_filters.UUIDFilter(field_name='grade__id', lookup_expr='exact')

    class Meta:
        model = Class
        fields = ["faculty", "grade"]


class TeacherClassFilter(django_filters.rest_framework.FilterSet):
    faculty = django_filters.UUIDFilter(field_name='faculty_id', lookup_expr='exact')
    grade = django_filters.UUIDFilter(field_name='grade__id', lookup_expr='exact')

    class Meta:
        model = TimeTable
        fields = ["faculty", "grade"]


class TeacherSubjectGroupFilter(django_filters.rest_framework.FilterSet):

    section = django_filters.UUIDFilter(field_name="section__id", lookup_expr="exact")
    faculty = django_filters.UUIDFilter(field_name="faculty__id", lookup_expr="exact")
    subject = django_filters.UUIDFilter(field_name="subject__id", lookup_expr="exact")

    class Meta:
        model = SubjectGroup
        fields = ["section", "subject", "faculty"]