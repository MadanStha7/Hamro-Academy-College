from academics.models import Faculty, Grade, Shift, Section, Subject
from timetable.administrator.serializers.timetable import (
    TimeTableSerializer,
    TimetableListSerialzer,
    TimeTableMultipleCreateSerializer,
)
from general.models import AcademicSession
from timetable.administrator.utils.create_timetable import (
    create_timetable,
    create_apply_timetable,
)
from timetable.models import Staff
from common.administrator.viewset import CommonInfoViewSet
from timetable.models import TimeTable
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from permissions.administrator import AdministratorPermission
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework import status
from django.db.models import F
from rest_framework import filters
from collections import defaultdict
from django.db import transaction
from rest_framework.exceptions import ValidationError
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
        day = self.request.query_params.get("day", False)

        queryset = TimeTable.objects.filter(institution=self.request.institution)
        if faculty:
            queryset = queryset.filter(faculty=faculty)
        if grade:
            queryset = queryset.filter(grade=grade)

        if section:
            queryset = queryset.filter(section=section)

        if shift:
            queryset = queryset.filter(shift=shift)

        if day:
            queryset = queryset.filter(day=day)
        queryset = queryset.annotate(
            subject__name=F("subject__name"),
            teacher__firstname=F("teacher__first_name"),
            teacher__lastname=F("teacher__last_name"),
        ).order_by("start_time")

        serializer = TimetableListSerialzer(queryset, many=True)
        timetables = defaultdict(list)
        for data in serializer.data:
            timetables[data["day_name"]].append(data)
        return Response(timetables)

    @action(detail=False, methods=["POST", "PUT"])
    def save_bulk_timetable(self, request):
        """ "
        Api to create bulk timetable and bulk update
        """
        faculty = self.request.query_params.get("faculty", False)
        grade = self.request.query_params.get("grade", False)
        shift = self.request.query_params.get("shift", False)
        section = self.request.query_params.get("section", False)
        day = self.request.query_params.get("day", False)

        if faculty:
            faculty_obj = get_object_or_404(
                Faculty, id=faculty, institution=self.request.institution
            )

        if grade:
            grade_obj = get_object_or_404(
                Grade, id=grade, institution=self.request.institution
            )

        if shift:
            shift_obj = get_object_or_404(
                Shift, id=shift, institution=self.request.institution
            )

        if section:
            section_obj = get_object_or_404(
                Section, id=section, institution=self.request.institution
            )
        else:
            section_obj = None

        if faculty_obj and grade_obj and shift_obj:
            list(
                map(
                    lambda data: data.update(
                        {
                            "faculty": faculty_obj,
                            "grade": grade_obj,
                            "shift": shift_obj,
                            "section": section_obj,
                            "day": day,
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
                    response["data1"] + response["data2"], many=True
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

    @action(detail=False, methods=["POST"])
    def apply_timetable(self, request):
        """
        Api to create bulk timetable based on the provided multiple days
        """
        with transaction.atomic():
            faculty = self.request.query_params.get("faculty", False)
            grade = self.request.query_params.get("grade", False)
            shift = self.request.query_params.get("shift", False)
            section = self.request.query_params.get("section", False)

            if faculty:
                faculty_obj = get_object_or_404(
                    Faculty, id=faculty, institution=self.request.institution
                )

            if grade:
                grade_obj = get_object_or_404(
                    Grade, id=grade, institution=self.request.institution
                )

            if shift:
                shift_obj = get_object_or_404(
                    Shift, id=shift, institution=self.request.institution
                )

            if section:
                section_obj = get_object_or_404(
                    Section, id=section, institution=self.request.institution
                )
            else:
                section_obj = None

            if faculty_obj and grade_obj and shift_obj:
                print("data", request.data["data"])
                print("data", type(request.data["data"]))
                for data in request.data["data"]:
                    data.update(
                        {
                            "faculty": faculty_obj,
                            "grade": grade_obj,
                            "shift": shift_obj,
                            "section": section_obj,
                        }
                    )
                print("ram", request.data)
                data = request.data["data"]
                serializer = TimetableListSerialzer(
                    data=request.data["data"], many=True
                )
                if serializer.is_valid():
                    response = create_apply_timetable(
                        request.data["data"],
                        request.data["days"],
                        self.request.user,
                        self.request.institution,
                    )
                    serializer = TimetableListSerialzer(response["data"], many=True)
                    if response:
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        {"error": serializer.errors},
                        status=status.HTTP_404_NOT_FOUND,
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
                        "full_name": teacher.first_name + " " + teacher.last_name,
                    }
                )
            return Response(teacher_data)

        else:
            return Response({"Teacher has not been added"})
