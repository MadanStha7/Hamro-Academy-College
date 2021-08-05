from academics.models import Faculty, Grade, Shift, Section
from timetable.administrator.serializers.timetable import (
    TimeTableSerializer,
    TimetableListSerialzer,
)
from timetable.administrator.utils.create_timetable import create_timetable
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from permissions.administrator import AdministratorPermission
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from timetable.models import Staff
from common.administrator.viewset import CommonInfoViewSet
from timetable.models import TimeTable
from rest_framework.decorators import action
from rest_framework import status
from django.db.models import F
from rest_framework import filters
import django_filters.rest_framework

User = get_user_model()


class TimeTableViewSet(CommonInfoViewSet):
    """
    CRUD for time table of the class
    """

    queryset = TimeTable.objects.none()
    serializer_class = TimeTableSerializer

    def list(self, request):
        """api to get list of timetable"""
        faculty = self.request.query_params.get("faculty", False)
        shift = self.request.query_params.get("shift", False)
        grade = self.request.query_params.get("grade", False)
        section = self.request.query_params.get("section", False)
        queryset = TimeTable.objects.filter(institution=self.request.institution)

        if faculty:
            queryset = queryset.filter(faculty__name__icontains=faculty)
        if grade:
            queryset = queryset.filter(grade__name=grade)

        if section:
            queryset = queryset.filter(section__name__icontains=section)

        if shift:
            queryset = queryset.filter(shift__name__icontains=shift)

        queryset = queryset.annotate(subject__name=F("subject__name"))
        serializer = TimetableListSerialzer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["POST", "PUT"])
    def save_bulk_timetable(self, request):
        """ "
        Add bulk timetable
        """
        faculty = self.request.query_params.get("faculty", False)
        grade = self.request.query_params.get("grade", False)
        shift = self.request.query_params.get("shift", False)
        section = self.request.query_params.get("section", False)
        # check if faculty object exist
        if faculty:
            try:
                faculty_obj = Faculty.objects.get(id=faculty)
            except Faculty.DoesNotExist:
                return Response(
                    {"error": ["faculty with this id doesn't exists"]},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"error": ["Faculty is required"]},
                status=status.HTTP_404_NOT_FOUND,
            )

        # check if grade object exist
        if grade:
            try:
                grade_obj = Grade.objects.get(id=grade)
            except Grade.DoesNotExist:
                return Response(
                    {"error": ["grade with this id doesn't exists"]},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"error": ["Grade is required"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # check if shift object exist
        if shift:
            try:
                shift_obj = Shift.objects.get(id=shift)
            except Shift.DoesNotExist:
                return Response(
                    {"error": ["shift with this id doesn't exists"]},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"error": ["Shift is required"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # check if section object exist
        print("section", section)
        if section:
            try:
                section_obj = Section.objects.get(id=section)
            except Section.DoesNotExist:
                section_obj = None
        else:
            section_obj = None
        if faculty_obj and grade_obj and shift_obj:
            print("section obj", section_obj)
            list(
                map(
                    lambda data: data.update(
                        {
                            "faculty": faculty_obj,
                            "grade": grade_obj,
                            "shift": shift_obj,
                            "section": section_obj,
                        }
                    ),
                    request.data,
                )
            )

            serializer = TimeTableSerializer(data=request.data, many=True)
            if serializer.is_valid():
                response = create_timetable(
                    request.data, self.request.user, self.request.institution
                )
                serializer = TimeTableSerializer(
                    response["timetable_create"], many=True
                )
                if response:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"error": serializer.errors},
                    status=status.HTTP_404_NOT_FOUND,
                )

        else:
            return Response(
                {"error": ["please provide the required field in query params"]},
                status=status.HTTP_400_BAD_REQUEST,
            )


class TeacherListView(APIView):
    """API to get list of all teachers of particular institution"""

    permission_classes = (IsAuthenticated, AdministratorPermission)

    def get(self, request):
        teachers = User.objects.filter(
            roles__title="Teacher", institution=self.request.institution
        )
        if teachers:
            teacher_data = []
            for teacher in teachers:
                teacher_data.append(
                    {
                        "id_of_teacher": teacher.id,
                        "full_name": teacher.first_name + "" + teacher.last_name,
                    }
                )
            return Response(teacher_data)

        else:
            return Response({"Teacher has not been added"})
